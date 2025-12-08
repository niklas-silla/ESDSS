import fitz # PyMuPD
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
import re
from rapidfuzz import fuzz
from collections import Counter
from llm_config import get_llm

class SectionCheckResult(BaseModel):
    """Result of Section Check Agent"""
    introduction: bool = Field(description="Section Introduction present: true or false")
    methods: bool = Field(description="Section Methods present: true or false")
    results: bool = Field(description="Section Results present: true or false")
    discussion: bool = Field(description="Section Discussion present: true or false")
    conclusion: bool = Field(description="Section Conclusion present: true or false")
    references: bool = Field(description="Section References present: true or false")
    section_report: str = Field(description="Short section report of max 50 words")

def section_check(md_manuscript_path):
    # 1. open markdown file
    with open(md_manuscript_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 2. build prompts with context
    system_prompt = """Y
        You are an expert in analyzing the structure of scientific manuscripts.

        Your task is to determine whether required scientific sections are present.
        A section is considered "present" if:
        - It appears as a heading, even under a different but semantically equivalent name,
        - OR it is merged with another section (e.g., "Results and Discussion"),
        - OR its content clearly occurs under another heading.

        A section is NOT present if:
        - It only appears as a brief mention,
        - Its presence is unclear or ambiguous.

        Typical variants:
        - Introduction → Background, Problem Statement
        - Methods → Methodology, Materials and Methods, Experimental Setup
        - Results → Findings, Outcomes
        - Discussion → Analysis, Interpretation
        - Conclusion → Summary, Closing Remarks
        - References → Bibliography, Works Cited, Literature
        
        Use only the content of the provided manuscript.
        If the presence of a section is ambiguous or uncertain, return false.
        Return ONLY the fields defined in the schema.
        Do not produce explanations outside the schema fields.
        """
    user_prompt = """
        Analyze the following manuscript and check whether the following scientific sections are present:
        - Introduction
        - Methods
        - Results
        - Discussion
        - Conclusion
        - References

        Use semantic equivalence and merged-section detection.
        Return true/false for each section, whether it is present or not.
        The section_report must summarize in max. 50 words, which sections are missing or merged.

        Manuscript:
        {manuscript_md}
        """
    
    # 3. invoke llm
    structured_llm = get_llm().with_structured_output(SectionCheckResult)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    chain = prompt | structured_llm
    analysis = chain.invoke({
        "manuscript_md": markdown_text
    })
    return analysis.model_dump() # return dict
    

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
    """Report of Format Agent"""
    report: str = Field(description="Concise format report of max 200 words")
    score: int = Field(ge=0, le=10, description="Format score 0-10")

def format_report_agent(formatting_results, presence_required_sections):
    
    # Build a prompt with context
    system_prompt = """
        You are an rigorous scientific reviewer for a scientific journal.

        Your task is to assess the formatting quality of a scientific manuscript based solely on the provided section-presence information and formatting-analysis results.  
        You must provide:
        1) A concise formatting report (maximum 200 words) describing the strengths and weaknesses.  
        2) A format score from 0 to 10, where:
            - 0 = very poor formatting; many required sections missing  
            - 10 = excellent formatting; all required sections present 

        Do not make assumptions beyond the supplied data.
        Return information strictly according to the fields defined in the output schema.
        Do not produce explanations outside the schema fields.
        """
    user_prompt = """
        Here are the analysis results:

        Presence of required sections:
        {presence_required_sections}

        Formatting analysis:
        {formatting_results}

        Based on these inputs, generate your formatting assessment.
        """
    
    # Invoke LLM
    structured_llm = get_llm().with_structured_output(FormatReport)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    chain = prompt | structured_llm
    response = chain.invoke({
        "presence_required_sections": presence_required_sections,
        "formatting_results": formatting_results
    })
    return response.model_dump()