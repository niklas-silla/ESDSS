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

# only a test node
def docling_node(state: AgentState) -> AgentState:
    """
    Docling node that analyzes and converts a PDF document into a md document and save it in the state.
    """
    source_path = "data/test_document.pdf"
    artifacts_path = "graph/nodes/docling/models" # path to docling models
    output_path = Path("data")
    # create output-folder if not exists
    output_path.mkdir(parents=True, exist_ok=True)

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

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # Convert the document
    doc = converter.convert(source_path).document

    # Export md document
    md_document = doc.export_to_markdown()
    with (output_path / "document.md").open("w") as f: 
        f.write(md_document)

    # Save images of figures and tables
    table_counter = 0
    picture_counter = 0
    image_dir = (output_path / "images") 
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path_list = []
    for element, _level in doc.iterate_items():
        if isinstance(element, TableItem):
            table_counter += 1
            image_path = (image_dir / f"table-{table_counter}.png")
            with image_path.open("wb") as fp:
                element.get_image(doc).save(fp, "PNG")
            image_path_list.append(str(image_path))
            
        elif isinstance(element, PictureItem):
            if element.get_image(doc).size[0] < 100 and element.get_image(doc).size[1] < 100:
                continue  # skip very small images
            picture_counter += 1
            image_path = (image_dir / f"picture-{picture_counter}.png")
            with image_path.open("wb") as fp:
                element.get_image(doc).save(fp, "PNG")
            image_path_list.append(str(image_path))

    # Update state
    state["md_document"] = f"{output_path}/document.md"
    state["number_of_tables"] = table_counter
    state["number_of_pictures"] = picture_counter
    state["images"] = image_path_list

    return state