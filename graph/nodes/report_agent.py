from graph.state import AgentState
from llm_config import get_llm
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

AGENT = "report_agent"

class FormatReport(BaseModel):
    deskreject: bool
    final_report: str

def report_generator_node(state: AgentState) -> AgentState:
    """
    Node to generate a report from all the agent analysis of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
  
    format_agent_report = state["format_agent"]["data"]["report"] + "\nScore: " + str(state["format_agent"]["data"]["score"])
    innovation_agent_report = state["innovation_agent"]["data"]["report"] + "\nScore: " + str(state["innovation_agent"]["data"]["score"])
    method_agent_report = state["method_agent"]["data"]["report"] + "\nScore: " + str(state["method_agent"]["data"]["score"])
    scopefit_agent_report = state["scopefit_agent"]["data"]["report"] + "\nScore: " + str(state["scopefit_agent"]["data"]["score"])
    quality_agent_report = state["quality_agent"]["data"]["report"] + "\nScore: " + str(state["quality_agent"]["data"]["score"])

    # Build system and user prompt 
    system_prompt = """
    You are the Final Report Agent. 
    Your task is to integrate evaluations from five specialized review agents and produce a concise, consistent, and academically sound summary report for a scientific manuscript. 
    You must analyze all inputs, weigh their relevance according to the rule set below, and produce a final decision: Desk Reject or No Desk Reject.

    WEIGHTING RULES:
    1. Scopefit Report = Highest priority. Out-of-scope issues can alone justify a Desk Reject.
    2. Innovation + Method Reports = High priority. Major weaknesses heavily influence the final decision.
    3. Quality + Format Reports = Medium priority. Important but rarely decisive if scope, innovation, and methods are strong. Minor issues should not drive a Desk Reject decision.

    Use scores only as qualitative signals, not mathematical operations.

    TASK:
    - Synthesize the five reports into a unified summary (max. ~10–12 sentences).
    - Highlight strengths and weaknesses with reference to the originating agent.
    - Explain the reasoning behind your final evaluation following the weighting rules.
    - Produce a final decision as a boolean: True = Desk Reject, False = No Desk Reject.
    - Produce a final textual summary in 'final_report'.
    """

    user_prompt = """
    Scopefit Agent Report:
    {scopefit_agent_report}

    Method Agent Report:
    {method_agent_report}

    Innovation Agent Report:
    {innovation_agent_report}

    Format Agent Report:
    {format_agent_report}

    Quality Agent Report:
    {quality_agent_report}
    """
    
    
    # Invoke LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    structured_llm = get_llm().with_structured_output(FormatReport)
    chain = prompt | structured_llm

    response = chain.invoke({
        "format_agent_report": format_agent_report,
        "innovation_agent_report": innovation_agent_report,
        "method_agent_report": method_agent_report,
        "scopefit_agent_report": scopefit_agent_report,
        "quality_agent_report": quality_agent_report,
    })

    state.update(response.model_dump())
    state[AGENT]["status"]= "success"
    
    return state