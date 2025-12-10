from llm_config import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import requests
import feedparser
import time
import re
import os
SEMANTIC_SCHOLAR_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

class InnovationStatementResult(BaseModel):
    """Result of Innovation Statement Agent"""
    innovation_statement: str = Field(description="Innovation statement of the manuscript.")
    search_queries: List[str] = Field(description="List of 2 search queries.")

def extract_innovation_statement(manuscript_md_path) -> dict:
        """extract innovation statement from the text"""

        # 1. open md file
        with open(manuscript_md_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        # 2. cut off all before Abstract, remove image tags and use only the first half of the manuscript (otherwise to much content -> Hallucination)
        markdown_text = re.split(r'##\s*\d*\s*\.?\s*Abstract', markdown_text, flags=re.IGNORECASE)[-1] # -1 -> everything after
        tokens = markdown_text.split() 
        half_index = len(tokens) // 2
        markdown_text = " ".join(tokens[:half_index])
        markdown_text = re.sub(r'<!-- image -->\n?', '', markdown_text)

        # 3. build prompt with context
        system_prompt = """
            You are an expert scientific analysis agent.
            Your task is to: 
            1) extract the core innovation of a scientific manuscript and
            2) generate 2 high-quality search queries that can be used to assess the novelty of that innovation. (max. 6 keywords)

            Use only the content of the provided manuscript!
            Return information strictly according to the output schema.
            Always answer in English!
            """
        user_prompt = """
            MANUSCRIPT:
            {markdown_text}

            Analyze the manuscript in the following structure:
            1. Extract the core innovation of the manuscript.
            2. Generate 2 short search queries to search for the presented innovation in the web.
            """
        
        
        # 4. invoke structured output llm 
        structured_llm = get_llm().with_structured_output(InnovationStatementResult, include_raw=True)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        chain = prompt | structured_llm
        analysis = chain.invoke({
            "markdown_text": markdown_text
        })
        # process raw data
        result = analysis["parsed"].model_dump() # convert Pydantic -> dict
        input_tokens = analysis["raw"].usage_metadata["input_tokens"]
        output_tokens = analysis["raw"].usage_metadata["output_tokens"]
        return result, input_tokens, output_tokens


def search_semantic_scholar(queries, max_results=5, max_retries=5) -> List:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {
        "x-api-key": SEMANTIC_SCHOLAR_API_KEY
    }
    results = []
    seen_ids = set()
    # request semantic scholar for each query in the queries list
    for q in queries:
        # skip empty queries
        if not q or not q.strip():
            continue

        params = {
            "query": q,
            "limit": max_results,
            "fields": "title,abstract"
        }
        # multiple attempts for response code 429 (to much requests per second -> retry)
        for attempt in range(max_retries):
            response = requests.get(url, params=params, headers=headers)
            time.sleep(1) # 1 request per second
            if response.status_code == 429:
                continue
            # other HTTP-Errors
            response.raise_for_status()
            # extract relevant data from response 
            data = response.json().get("data", [])
            for item in data:
                id = item.get("paperId")
                if item.get("paperId") not in seen_ids and id is not None:
                    results.append({"title": item.get("title", ""), "abstract": item.get("abstract", "")})
            break

    return results


def search_arxiv(queries, max_results=5, max_retries=5) -> List:
    base_url = "http://export.arxiv.org/api/query?"
    results = []
    seen_ids = set()
    # request arxiv for each query in the queries list
    for q in queries:
        # skip empty queries
        if not q or not q.strip():
            continue

        search_query = f"search_query=all:{q}&start=0&max_results={max_results}"
        response = requests.get(base_url + search_query)
        feed = feedparser.parse(response.text)
        # extract relevant data from response 
        for entry in feed.get("entries"):
            results.append({
                "title": entry.get("title"),
                "abstract": entry.get("summary"),
            })
    return results


class InnovationReport(BaseModel):
    """Report of Innovation Agent"""
    report: str = Field(description="Concise innovation report of max 200 words")
    score: int = Field(ge=0, le=10, description="Innovation score 0-10")


def innovation_report_agent(innovation_statement, web_results_semschol, web_results_arxiv):
    
    # 1. Build prompt
    system_prompt = """
        You are an rigorous scientific reviewer for a scientific journal.

        Your task is to assess the novelty of a manuscript’s core innovation using the provided search results from Semantic Scholar and arXiv.
        You must provide:
        1) A concise innovation report (maximum 200 words) describing whether the manuscript innovation is novel or not.
        2) A innovation score from 0 to 10, where:
            - 0 = not novel  
            - 10 = highly novel

        Do not make assumptions beyond the supplied data.
        Return information strictly according to the fields defined in the output schema.
        Do not produce explanations outside the schema fields.
        Always answer in English!
        """
    user_prompt = """
        Here are the analysis results:

        Manuscript Innovation:
        {core_innovation}

        Websearch Results:
        {websearch_results}

        Based on these inputs, generate your innovation assessment.
        """
    
    # 2. Prepare strings of search results
    websearch_results = web_results_semschol + web_results_arxiv
    websearch_results = "\n".join([f"{r.get('title')}: {r.get('abstract','')}" for r in websearch_results])
    
    # 3. Invoke LLM and generate report
    llm = get_llm().with_structured_output(InnovationReport, include_raw=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
        ])
    chain = prompt | llm
    response = chain.invoke({
        "core_innovation": innovation_statement,
        "websearch_results": websearch_results
    })
    # process raw data
    result = response["parsed"].model_dump() # convert Pydantic -> dict
    input_tokens = response["raw"].usage_metadata["input_tokens"]
    output_tokens = response["raw"].usage_metadata["output_tokens"]
    return result, input_tokens, output_tokens
