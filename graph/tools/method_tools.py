import re
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm_config import get_embedding, get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
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


class MethodCheckResult(BaseModel):
    research_question: str
    rq_report: str
    methodology_report: str
    score: int

def method_analysis(vectorstore) -> dict:
        """Analyse the research question, methodology and implementation"""
        
        retrieval_queries = {
            "research_question": "research question hypothesis aim objective purpose goal",
            "methodology": "methodology methods approach design procedure experimental setup",
        }

        # 1. retrieve all relevant sections for each query
        contexts = {}
        for key, query in retrieval_queries.items():
            sections = vectorstore.similarity_search(query, k=10)
            contexts[key] = "\n\n".join(sec.page_content for sec in sections)
        
        # 2. build prompt with context
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
            "You are a senior reviewer for a scientific journal. "
            "Provide a rigorous, critical, structured assessment. "
            "Use only the provided manuscript excerpts."),

            ("user",
            "=== CONTEXT: RESEARCH QUESTION ===\n{rq_context}\n\n"
            "=== CONTEXT: METHODOLOGY ===\n{method_context}\n\n"
            "Analyze the manuscript in the following structure:\n\n"
            "1. Extract the research question precisely.\n"
            "2. Assess the quality, clarity and scientific rigor of the research question (max 100 words).\n"
            "3. Assess the methodological rigor, appropriateness and design (max 150 words).\n"
            "4. Provide a final Score: 0 to 10.\n\n")
        ])
        
        # 3. generate analysis with llm
        structured_llm = llm.with_structured_output(MethodCheckResult)
        chain = prompt | structured_llm 
        analysis = chain.invoke({
            "rq_context": contexts["research_question"],
            "method_context": contexts["methodology"]
        })
        
        # 4. structure report
        report = {
             "researchquestion": analysis.research_question,
             "report": analysis.rq_report + "\n" + analysis.methodology_report,
             "score": analysis.score
        }
        return report
