import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" # required
import numpy as np
from pathlib import Path
from llm_config import get_llm, get_embedding
from pydantic import BaseModel, Field
from langchain_community.vectorstores import FAISS
import fitz # PyMuPDF
import re
from langchain_core.prompts import ChatPromptTemplate

embeddings = get_embedding()
current_dir = Path(__file__).parent
vectorstore_path = current_dir / "vectorstore_em_paper_OpenAI" # change vector db folder here (vectorstore_em_paper_Ollama / vectorstore_em_paper_OpenAI)

vector_store = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

def normalize_spaces(text: str) -> str:
    # Liste üblicher Sonder-Leerzeichen
    special_spaces = [
        "\u00A0",  # No-break space (NBSP)
        "\u2000",  # En quad
        "\u2001",  # Em quad
        "\u2002",  # En space
        "\u2003",  # Em space
        "\u2004",  # Three-per-em space
        "\u2005",  # Four-per-em space
        "\u2006",  # Six-per-em space
        "\u2007",  # Figure space
        "\u2008",  # Punctuation space
        "\u2009",  # Thin space
        "\u200A",  # Hair space
        "\u202F",  # Narrow no-break space
        "\u205F",  # Medium mathematical space
        "\u3000",  # Ideographic space
    ]

    for s in special_spaces:
        text = text.replace(s, " ")
    return text


def extract_manuscript_data(path) -> dict[str,str]:
    # open doc and extract first two pages
    doc = fitz.open(path)
    text = ""
    for page in doc[:2]:
        t = doc[0].get_text("text")
        lines = t.splitlines()
        text += "\n".join(lines[:-1]) # remove last line "Powered by Editorial Manager® ..."
    
    title_pattern = r"Full Title:\s*(.*?)\s*(Article Type:)"
    title_match = re.search(title_pattern, text, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip().replace("\n", " ") if title_match else None

    abstract_pattern = r"Abstract:\s*(.*?)\s*(?=Title Page|Click here|$)"
    abstract_match = re.search(abstract_pattern, text, re.DOTALL | re.IGNORECASE)
    abstract = abstract_match.group(1).strip().replace("\n", " ") if abstract_match else None

    if title is None:
        title = text
    if abstract is None:
        abstract = text

    title = normalize_spaces(title)
    abstract = normalize_spaces(abstract)

    return {"title": title,"abstract": abstract}


def cosine_similarity(text1, text2) -> float:
    v1 = embeddings.embed_query(text1)
    v2 = embeddings.embed_query(text2)
    cosine_similarity_value = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return cosine_similarity_value


def calculate_cosine_similarity(manuscript_data):
    # find 10 nearest neighbors in the vexctorstore
    neighbors = vector_store.similarity_search(manuscript_data["title"], k=10)

    title_cs_scores = []
    abstract_cs_scores = []
    neighbor_info = ""
    for n in neighbors:
        # calculate cosine_similarity between manuscript title and vector text
        title_cs = cosine_similarity(manuscript_data["title"], n.page_content)
        title_cs_scores.append(title_cs)
        # calculate cosine_similarity between manuscript title and vector text
        abstract_cs = cosine_similarity(manuscript_data["abstract"], n.metadata["abstract"])
        abstract_cs_scores.append(abstract_cs)
        # prepare neighbor data for LLM 
        neighbor_info += f"{n.page_content} - Score={round(title_cs, 2)}\n"

    title_cs_median = round(np.median(title_cs_scores), 2)
    abstract_cs_median = round(np.median(abstract_cs_scores), 2)

    return {"neighbor_info": neighbor_info, "title_cs_median": title_cs_median, "abstract_cs_median": abstract_cs_median}


class ScopefitReport(BaseModel):
    """Report of Scopefit Agent"""
    report: str = Field(description="Concise scope-fit report of max 200 words")
    score: int = Field(ge=0, le=10, description="Scope-fit score 0-10") 


def generate_scopefit_report(manuscript_data: dict, neighbor_info: str, title_cs_median: float, abstract_cs_median: float) -> dict:
    
    aim_scope_em = """
        Electronic Markets (EM) is a leading academic journal that offers a forum for research on all forms of networked business. EM recognizes the transformational role of information and communication technology (IT) in changing the interaction between organizations and customers, which is present in social networks, electronic commerce, supply chain management, or customer relationship management. Electronic markets, in particular, refer to forms of networked business where multiple suppliers and customers interact for economic purposes within one or among multiple tiers in economic value chains. As a broad concept, there are many forms of electronic markets: In a narrow sense, electronic markets are mainly conceived as allocation platforms with dynamic price discovery mechanisms involving atomistic relationships. Popular examples originate from the financial (e.g., CBOT, XETRA) and energy markets (e.g., EEX, ICE).    
        In a broader sense, price discovery is not critical for Electronic Markets. These solutions emphasize longer-term relationships and processes for enabling business transactions (e.g., electronic procurement solutions) and/or knowledge management (e.g., product development, problem and incident management). EM covers diverse aspects of networked business and welcomes research from a technological, organizational, societal, and/or political perspective. Since EM is a methodologically pluralistic journal, quantitative and qualitative research methods are both welcome as long as the studies are methodologically sound. Conceptual and theory-development papers, empirical hypothesis testing, and case-based studies are all welcome.
        """

    system_prompt = """
        You are an rigorous scientific reviewer for a scientific journal.
        
        Your task is to assess whether a new manuscript fits the scope of the Electronic Markets (EM) Journal.
        Your assessment must be based exclusively on the input data provided in the user prompt. 
        Use qualitative reasoning (scope text + semantic neighbors) and quantitative reasoning (cosine similarity).

        The user will provide the following inputs:
        1) The manuscript title and abstract  
        2) Ten semantic nearest-neighbor EM publications, including their titles and cosine similarity scores  
        3) Median cosine similarity metrics (title-level and abstract-level)  
        4) The official Aim & Scope text of the Electronic Markets Journal  
        
        You must provide:
        1) A concise scope-fit report (maximum 200 words) evaluating whether the manuscript fits EM's scope.  
        2) A scope-fit score from 0 to 10, where:
            - 0 = very poor scope-fit  
            - 10 = excellent scope-fit 

        Do not make assumptions beyond the supplied data.
        Return information strictly according to the fields defined in the output schema.
        Do not produce explanations outside the schema fields.
        Always answer in English!
        """
                            

    user_prompt = f"""
        Below is all information you may use for your assessment.  
        Base your judgment strictly and exclusively on these inputs.

        1. New Manuscript Information
        Title: {manuscript_data["title"]}
        Abstract: {manuscript_data["abstract"]}

        2. Semantic Nearest Neighbor Publications from the EM Vectorstore
        Ten closest semantic neighbors (title + cosine similarity to the manuscript title):
        {neighbor_info}

        3. Similarity Metrics
        Median cosine similarity (title comparison): {title_cs_median}
        Median cosine similarity (abstract comparison): {abstract_cs_median}

        4. Official Aim & Scope of the Electronic Markets Journal
        {aim_scope_em}
                
        Based on these inputs, generate your scope-fit assessment.
        """

    # Invoke LLM
    structured_llm = get_llm().with_structured_output(ScopefitReport, include_raw=True)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    chain = prompt | structured_llm
    response = chain.invoke({
        "manuscript_data": manuscript_data,
        "neighbor_info": neighbor_info,
        "title_cs_median": title_cs_median,
        "abstract_cs_median": abstract_cs_median,
        "aim_scope_em": aim_scope_em
    })
    # process raw data
    result = response["parsed"].model_dump()
    input_tokens = response["raw"].usage_metadata["input_tokens"]
    output_tokens = response["raw"].usage_metadata["output_tokens"]
    return result, input_tokens, output_tokens
