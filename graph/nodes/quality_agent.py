from graph.state import AgentState
from llm_config import get_llm
from graph.tools.quality_tools import analyze_images, compute_readability_scores, generate_quality_report
from langgraph.graph import StateGraph, START, END

def quality_check_node(state: AgentState) -> AgentState:
    """
    Node to check the quality aspects of a PDF manuscript.
    """
    agent_name="quality_agent"
    state[agent_name]["status"]= "running"

    state = sub_graph.invoke(state)

    state[agent_name]["status"]= "success"
    return state[agent_name]


# -----------
#  Sub Nodes
# -----------
def analyze_images_node(state: AgentState):
    state["quality_agent"]["data"]["imagequality"] = analyze_images(state["images"])
    return state

def readability_node(state: AgentState):
    state["quality_agent"]["data"]["textquality"] = compute_readability_scores(state["md_manuscript_path"])
    return state

def report_node(state: AgentState):
    result = state["quality_report"] = generate_quality_report(
        state["quality_agent"]["data"]["imagequality"],
        state["quality_agent"]["data"]["textquality"]
    )
    state["quality_agent"]["data"].update(result)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("analyze_images", analyze_images_node)
quality_graph.add_node("readability", readability_node)
quality_graph.add_node("report", report_node)

quality_graph.add_edge(START, "analyze_images")
quality_graph.add_edge("analyze_images", "readability")
quality_graph.add_edge("readability", "report")
quality_graph.add_edge("report", END)

sub_graph = quality_graph.compile()
