from graph.state import AgentState
# for using prefetced models of docling
from docling.datamodel.base_models import InputFormat 
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
# for document conversion with docling
from docling.document_converter import DocumentConverter, PdfFormatOption
# for configuring picture description
from docling.datamodel.pipeline_options import PictureDescriptionVlmOptions
# for extracting pictures and tables
from docling_core.types.doc import PictureItem, TableItem
from pathlib import Path
import fitz  # PyMuPDF library for PDF processing
import re # regular expressions


def manuscript_preprocessing_node(state: AgentState) -> AgentState:
    """
    Node to preprocess a PDF manuscript.
    """
    agent_name="preprocessing"
    state[agent_name]["status"]= "running"
    print("Preprocessing runs ...")

    pdf_path = state["manuscript_path"]
    preprocessed_pdf_path = Path("data/preprocessed_manuscript.pdf")
    output_path = Path("data")

    # Step 1: preprocess manuscript for better docling conversion 
    doc = fitz.open(pdf_path)
    doc = cut_off_cover_pages(doc)
    doc = remove_linenumbers_and_headers(doc)
    doc.save(preprocessed_pdf_path)
    doc.close()

    # Step 2: Convert with Docling
    result = docling_converter(preprocessed_pdf_path, output_path)

    # Step 3: update state
    state["md_manuscript_path"] = result["md_manuscript_path"]
    state["number_of_tables"] = result["number_of_tables"]
    state["number_of_pictures"] = result["number_of_pictures"]
    state["images"] = result["images"]
    
    state[agent_name]["status"]= "success"
    return state


def cut_off_cover_pages(doc: fitz.Document) -> fitz.Document:
    """
    Function to cut off cover pages of a PDF manuscript.
    """

    # 1. variables to track page indices
    last_titlepage_index = None
    start_blindedmanuscript_index = None

    # 2. check first pages for "Title Page" and "Blinded Manuscript"
    for i, page in enumerate(doc):
        text = page.get_text("text")  # extract text from page
        if "title page" in text.lower() and last_titlepage_index is None:
            last_titlepage_index = i
        if "blinded manuscript" in text.lower() and start_blindedmanuscript_index is None:
            start_blindedmanuscript_index = i

    # 3. determine the index to keep from
    if start_blindedmanuscript_index is None:
        print("No page with 'Blinded Manuscript' found.")
        return doc # return original file if no 'Blinded Manuscript' found
    elif last_titlepage_index is None:
        print("No page with 'Title Page' found.")
        return doc # return original file if no 'Title Page' found
    elif last_titlepage_index + 1 != start_blindedmanuscript_index:
        print(f"Can't determine cut-off point reliably. Last 'Title Page' at index {last_titlepage_index}, 'Blinded Manuscript' at index {start_blindedmanuscript_index}.")
        return doc # return original file if cut-off point is unclear
    
    print(f"Cut-off point after page {last_titlepage_index + 1}")

    # 4. delete pages before "Blinded Manuscript"
    if start_blindedmanuscript_index > 0:
        doc.delete_pages(0, start_blindedmanuscript_index - 1)
        print("Cover pages were cut off.")

    return doc


def remove_linenumbers_and_headers(doc: fitz.Document) -> fitz.Document:
    """
    Function to remove line numbers and headers from a PDF manuscript.
    """

    # iterate through pages and remove line numbers and headers
    for page in doc:
        # --- Line Numbers ---
        left_column_rect = fitz.Rect(0, 0, 30, page.rect.height)
        page.add_redact_annot(left_column_rect, fill=(1, 1, 1))

        # --- Headers ---
        header_rect = fitz.Rect(0, 0, page.rect.width, 60)
        page.add_redact_annot(header_rect, fill=(1, 1, 1))

        page.apply_redactions()

    print("Linenumbers & Headers removed.")

    return doc


def docling_converter(input_path: str, output_path: Path) -> tuple[str, int, int, list[str]]:
    """
    Docling Function to analyze and convert a PDF document into a md document.
    """
    
    # 1. set up document converter with desired options
    artifacts_path = "graph/nodes/docling/models" # path to docling models
    pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path,
                                          do_table_structure=True)
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE  # use more accurate TableFormer model
    pipeline_options.do_code_enrichment = True # enable code enrichment
    pipeline_options.do_formula_enrichment = True # enable formula enrichment

    pipeline_options.generate_picture_images = True
    pipeline_options.generate_page_images = True
    pipeline_options.images_scale = 2  # scale images by factor 2
    pipeline_options.do_picture_classification = True # enable picture classification

    pipeline_options.do_picture_description = True # enable picture description
    pipeline_options.picture_description_options = PictureDescriptionVlmOptions(
        repo_id="models--HuggingFaceTB--SmolVLM-256M-Instruct",
        prompt="Describe the image in three sentences. Be concise and accurate.",
    )

    # 2. create document converter
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # 3. Convert the document
    docling_doc = converter.convert(input_path).document

    # 4. Export md manuscript
    md_document = docling_doc.export_to_markdown()

    # 5. clean and save md document
    md_document = clean_markdown(md_document)
    
    with (output_path / "manuscript.md").open("w") as f: 
        f.write(md_document)

    # 5. Save images of figures and tables
    table_counter = 0
    picture_counter = 0
    image_dir = (output_path / "images") 
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path_list = []
    for element, _level in docling_doc.iterate_items():
        if isinstance(element, TableItem):
            table_counter += 1
            image_path = (image_dir / f"table-{table_counter}.png")
            with image_path.open("wb") as fp:
                element.get_image(docling_doc).save(fp, "PNG")
            image_path_list.append(str(image_path))
            
        elif isinstance(element, PictureItem):
            if element.get_image(docling_doc).size[0] < 100 and element.get_image(docling_doc).size[1] < 100:
                continue  # skip very small images
            picture_counter += 1
            image_path = (image_dir / f"picture-{picture_counter}.png")
            with image_path.open("wb") as fp:
                element.get_image(docling_doc).save(fp, "PNG")
            image_path_list.append(str(image_path))

    # 6. return results
    return {"md_manuscript_path": output_path / "manuscript.md", "number_of_tables": table_counter, "number_of_pictures": picture_counter, "images": image_path_list}


def clean_markdown(md_text: str) -> str:
    """
    Clean the markdown text by removing unwanted formatting issues.
    """
    # remove unwanted patterns like <!-- ... -->
    md_text = re.sub(r'<!--.*?-->', '', md_text, flags=re.DOTALL)

    # remove multiple spaces and newlines
    md_text = re.sub(r'[ \t]+', ' ', md_text)
    md_text = re.sub(r'\n{3,}', '\n\n', md_text)

    # remove leading and trailing whitespace
    md_text = md_text.strip()
    return md_text