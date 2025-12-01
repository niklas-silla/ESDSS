import fitz # PyMuPD
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
import re
from rapidfuzz import fuzz
from collections import Counter
from llm_config import get_llm

class SectionCheckResult(BaseModel):
    introduction: bool
    methods: bool
    results: bool
    discussion: bool
    conclusion: bool
    references: bool
    section_report: str

def section_check(md_manuscript_path):
    with open(md_manuscript_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 2. build prompt with context
    prompt = ChatPromptTemplate.from_messages([
        ("user",
        """
        MANUSCRIPT:
        {manuscript_md}

        You are an expert scientific analysis agent.
        Your task is to check whether all required sections of a scientific paper are present in the Manuscript, regardless of their exact wording, numbering, or formatting.
        Check the provided manuscript text for the following required sections:
        - Introduction
        - Methods
        - Results
        - Discussion
        - Conclusion
        - References

        Consider alternative spellings, numbering styles, subheadings, and different Markdown heading levels.
        Return for each section, whether it is present or not (true or false).
        Additional give a short report of max. 50 words.
        """
        )
    ])
    
    structured_llm = get_llm().with_structured_output(SectionCheckResult)
    chain = prompt | structured_llm
    analysis = chain.invoke({
        "manuscript_md": markdown_text
    })
    return analysis.model_dump()
    

def formatting_check(preprocessed_manuscript_path, md_path):

    # 1. extract all textblocks of PDF
    pdf_textblocks = []
    doc = fitz.open(preprocessed_manuscript_path)
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    pdf_textblocks.append({
                        "text": span["text"],
                        "font": span["font"],
                        "size": str(span["size"])
                    })
    
    # A: HEADING CHECK

    # 2. find all headings in markdown file
    headings = []
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        # Matcht "# Heading", "## Heading", "### Heading"
        match = re.match(r"^(#{1,3})\s+(.*)", line)
        if match:
            title = match.group(2).strip()
            headings.append(title)
    # remove EM letters
    headings.pop(0) # Electronic Markets - The International Journal on Networked Business
    headings.pop(0) # [Manuscript]

    # 3. combine headings with their metadata and check formatting
    checked_headings = []
    correct_headings = 0
    all_checked_headings = 0
    for h in headings:
        for block in pdf_textblocks:
            if fuzz.ratio(h, block["text"]) >= 90:
                all_checked_headings += 1
                size = round(float(block["size"]))
                font = block["font"]
                formatting = ""
                # check formating fit
                if "Times New Roman" in font:
                    if size == 18:
                        formatting = "Correct formatting (H1)"
                        correct_headings += 1
                    elif size == 14:
                        formatting = "Correct formatting (H2)"
                        correct_headings += 1
                    elif size == 10:
                        formatting = "Correct formatting (H3)"
                        correct_headings += 1
                    else:
                        formatting = f"Incorrect formatting (size={size})"
                else:
                    formatting = f"Incorrect formatting (font={font})"

                checked_headings.append({
                    "text": h,
                    "font": font,
                    "size": size,
                    "formatting": formatting
                })
                break # found -> next heading


    # B: MAIN TEXT CHECK

    # extract all sizes
    sizes = [round(float(item["size"])) for item in pdf_textblocks]
    fonts = [item["font"] for item in pdf_textblocks]
    # count frequencies
    size_counter = Counter(sizes)
    font_counter = Counter(fonts)
    # return the most frequent value
    most_frequent_size = size_counter.most_common(1)[0][0]
    most_frequent_font = font_counter.most_common(1)[0][0]

    if most_frequent_size == 10:
        main_text_size = "The font size of the text matches the stylesheet of 10 pt."
    else:
        main_text_size = f"The font size of the text does not match the stylesheet and is {most_frequent_size} instead of 10pt."

    if "Times New Roman" in most_frequent_font:
        main_text_font = "The font of the text matches the stylesheet of Times New Roman."
    else:
        main_text_font = f"The font of the text does not match the stylesheet and is {most_frequent_font} instead of Times New Roman."


    # C: COMBINE RESULTS

    results_headings = "\n".join(f"{h['text']}: {h['formatting']}" for h in checked_headings)
    format_report = (
        "HEADING FORMATTING:\n"
        f"{results_headings}\n"
        f"{correct_headings} headings are correct of {all_checked_headings} checked headings.\n\n"
        "TEXT FORMATTING:\n"
        f"{main_text_size}\n"
        f"{main_text_font}"
        )
    return format_report


class FormatReport(BaseModel):
    report: str
    score: int

def format_report_agent(formatting_results, presence_required_sections):
    
    # Build a prompt with context
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        """
        You are an expert scientific reviewer.
        Your task is to assess the format of a scientific manuscript based on the completeness of the required sections and the formatting results of headings and text.
        Provide a short report (max 200 words) and a format score from 0 (poor formatting and many required sections missing) to 10 (perfect formatting and all required sections present).
        """
        ),
        ("user",
        """
        Presence Required sections:
        {presence_required_sections}

        Formatting Results:
        {formatting_results}

        Based on these results, decide about the manuscript formating. 
        """
        )
    ])
    
    # Invoke LLM
    structured_llm = get_llm().with_structured_output(FormatReport)
    chain = prompt | structured_llm
    response = chain.invoke({
        "presence_required_sections": presence_required_sections,
        "formatting_results": formatting_results
    })
    return response.model_dump()