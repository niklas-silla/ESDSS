from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.quality_tools import analyze_images, compute_readability_scores, generate_quality_report
from langgraph.graph import StateGraph, START, END

AGENT="quality_agent"

def quality_check_node(state: AgentState) -> AgentState:
    """
    Node to check the quality aspects of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
    try:
        state = sub_graph.invoke(state)
        state[AGENT]["status"]= "success"
    except Exception as e:
        state[AGENT]["status"]= "failed"
        state[AGENT]["error"].append(e)
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def analyze_images_node(state: AgentState):
    state[AGENT]["data"]["imagequality"] = analyze_images(state["images"])
    return state

def readability_node(state: AgentState):
    state[AGENT]["data"]["textquality"] = compute_readability_scores(state["md_manuscript_path"])
    return state

def report_node(state: AgentState):
    report = generate_quality_report(
        state[AGENT]["data"]["imagequality"],
        state[AGENT]["data"]["textquality"]
    )
    state[AGENT]["data"].update(report)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("analyze_images", analyze_images_node)
quality_graph.add_node("calculate_readability", readability_node)
quality_graph.add_node("generate_report", report_node)

quality_graph.add_edge(START, "analyze_images")
quality_graph.add_edge("analyze_images", "calculate_readability")
quality_graph.add_edge("calculate_readability", "generate_report")
quality_graph.add_edge("generate_report", END)

sub_graph = quality_graph.compile()
visualize_graph_png(graph = sub_graph, filename = "quality_agent_subgraph.png")
