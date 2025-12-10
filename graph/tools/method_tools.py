import re
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm_config import get_embedding, get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from pathlib import Path

embedding = get_embedding()
llm = get_llm()

vectorstore_path = Path("data/vectorstore_manuscript")

def create_vectorstore(md_path) -> FAISS:
    """
    Splits a markdownfile in chunks to create a vectorstore.
    """
    # load md_file
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # cut off all from reference section and remove image tags
    markdown_text = re.split(r'##\s*References\s*List', markdown_text, flags=re.IGNORECASE)[0]
    markdown_text = re.sub(r'<!-- image -->\n?', '', markdown_text)

    # splits at the headers
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on,
        strip_headers = True)
    md_header_splits = markdown_splitter.split_text(markdown_text)

    # create chunks according to the separators
    separators=[
        "\n\n",
        "\n",
        " ",
    ]
    chunk_size = 1000
    chunk_overlap = 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, chunk_overlap=chunk_overlap, separators=separators
    )
    chunks = text_splitter.split_documents(md_header_splits)
    
    # create vectorstore
    vectorstore = FAISS.from_documents(chunks, embedding)
    return vectorstore


class MethodReport(BaseModel):
    """Report of Method Agent"""
    research_question: str = Field(description="Extracted research question of the manuscript")
    rq_report: str = Field(description="Concise research question report of max 100 words")
    methodology_report: str = Field(description="Concise methodology report of max 100 words")
    score: int = Field(ge=0, le=10, description="Methodology score 0-10")

def method_analysis(vectorstore) -> dict:
        """Analyse the research question, methodology and implementation"""
        
        # define retrieval queries
        retrieval_queries = {
            "research_question": "research question hypothesis aim objective purpose goal",
            "methodology": "methodology methods approach design procedure experimental setup",
        }

        # retrieve all relevant sections for each query
        context = {}
        for key, query in retrieval_queries.items():
            sections = vectorstore.similarity_search(query, k=15)
            context[key] = "\n\n".join(sec.page_content for sec in sections)
        
        return context

def method_report_agent(context):
        # 2. build prompt with context
        system_prompt = """
            You are an rigorous scientific reviewer for a scientific journal.

            Your task is to analyze the manuscript based on the content provided in the following structure:
            1) Extract the research question precisely.
            2) Assess the quality, clarity and scientific rigor of the research question in a short report (max 100 words).
            3. Assess the methodological rigor, appropriateness and design in a short report (max 100 words).
            4. Provide a methodology score from 0 to 10, where:
                - 0 = completely flawed, inappropriate, or non-scientific methodology
                - 10 = fully rigorous, appropriate, and methodologically exemplary design

            Do not make assumptions beyond the supplied data.
            Return information strictly according to the fields defined in the output schema.
            Do not produce explanations outside the schema fields.
            Always answer in English!
            """
        user_prompt = """
            Here are the relevant content of the manuscript:

            Content related to the research question:
            {rq_context}

            Content related to the methodology
            {method_context}

            Based on these inputs, generate your methodology assessment.
            """
        
        
        # 3. generate analysis with llm
        structured_llm = llm.with_structured_output(MethodReport, include_raw=True)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        chain = prompt | structured_llm 
        analysis = chain.invoke({
            "rq_context": context["research_question"],
            "method_context": context["methodology"]
        })
        
        # process raw data
        result = analysis["parsed"]
        input_tokens = analysis["raw"].usage_metadata["input_tokens"]
        output_tokens = analysis["raw"].usage_metadata["output_tokens"]

        # 4. structure report
        report = {
             "researchquestion": result.research_question,
             "report": result.rq_report + "\n" + result.methodology_report,
             "score": result.score
        }
        return report, input_tokens, output_tokens
