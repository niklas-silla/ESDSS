from llm_config import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
import requests
import feedparser
import time
import re

class InnovationStatementResult(BaseModel):
    innovation_statement: str
    search_queries: List[str]

def extract_innovation_statement(manuscript_md_path) -> dict:
        """extract innovation statement from the text"""

        # 1. open md file
        with open(manuscript_md_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        # 2. cut off all from reference section and remove image tags
        markdown_text = re.split(r'##\s*References\s*List', markdown_text, flags=re.IGNORECASE)[0]
        markdown_text = re.sub(r'<!-- image -->\n?', '', markdown_text)

        # 3. build prompt with context
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            """
            You are an expert scientific analysis agent.
            Your task is to (1) extract the core innovation of a scientific manuscript and (2) generate high-quality search queries that can be used to assess the novelty of that innovation.
            Use only the provided manuscript text!
            """
            ),
            ("user",
            """
            MANUSCRIPT:
            {markdown_text}

            Analyze the manuscript in the following structure:
            1. Extract the core innovation of the manuscript.
            2. Generate 2 short search queries consisting of keywords (max 6 words) to search for the presented innovation in the web.
            The search queries should collectively cover the innovation statement of the manuscript.
            """
            )
        ])
        
        # 4. invoke structured output llm 
        structured_llm = get_llm().with_structured_output(InnovationStatementResult)
        chain = prompt | structured_llm
        analysis = chain.invoke({
            "markdown_text": markdown_text
        })
        
        return analysis.model_dump() # convert Pydantic -> dict


def search_semantic_scholar(queries, max_results=5, max_retries=5) -> List:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {
        "x-api-key": "9qI5TDajbT2eKQH3mrZIZ64mkdjUx12lyVlE2fVf"
    }
    results = []
    seen_ids = set()
    # request semantic scholar for each query in the queries list
    for q in queries:
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


class InnovationCheckResult(BaseModel):
    report: str
    score: int


def innovation_report_agent(innovation_statement, web_results_semschol, web_results_arxiv):
    
    # 1. Build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        """
        You are an expert scientific reviewer.
        Your task is to assess the novelty of a scientific innovation based on search results from Semantic Scholar and arXiv.
        Provide a short report (max 200 words) and a novelty score from 0 (not novel) to 10 (highly novel).
        """
        ),
        ("user",
        """
        Manuscript Innovation:
        {core_innovation}

        Websearch Results:
        {websearch_results}

        Based on these results, decide if the manuscript innovation is novel. 
        Return a innovation score (0-10) and a innovation report (max 200 words)
        """
        )
    ])
    
    # 2. Prepare strings of search results
    websearch_results = web_results_semschol + web_results_arxiv
    websearch_results = "\n".join([f"{r.get('title')}: {r.get('abstract','')}" for r in websearch_results])
    
    # 3. Invoke LLM and generate report
    llm = get_llm().with_structured_output(InnovationCheckResult)
    chain = prompt | llm
    response = chain.invoke({
        "core_innovation": innovation_statement,
        "websearch_results": websearch_results
    })
    
    return response.model_dump() # convert Pydantic -> dict
