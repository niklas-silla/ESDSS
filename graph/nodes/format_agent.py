from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.format_tools import formatting_check, section_check, format_report_agent
from langgraph.graph import StateGraph, START, END

AGENT = "format_agent"

def format_check_node(state: AgentState) -> AgentState:
    """
    Node to check the format of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
    
    state = sub_graph.invoke(state)
    
    state[AGENT]["status"]= "success"
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def section_check_node(state: AgentState):
    state[AGENT]["data"]["section_check"] = section_check(state["md_manuscript_path"])
    return state

def formatting_check_node(state: AgentState):
    state[AGENT]["data"]["formatting_check"] = formatting_check(state["preprocessed_manuscript_path"], state["md_manuscript_path"])
    return state

def format_report_node(state: AgentState):
    report = format_report_agent(state[AGENT]["data"]["formatting_check"], state[AGENT]["data"]["section_check"])
    state[AGENT]["data"].update(report)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("section_check", section_check_node)
quality_graph.add_node("formatting_check", formatting_check_node)
quality_graph.add_node("report", format_report_node)

quality_graph.add_edge(START, "section_check")
quality_graph.add_edge("section_check", "formatting_check")
quality_graph.add_edge("formatting_check", "report")
quality_graph.add_edge("report", END)

sub_graph = quality_graph.compile()
visualize_graph_png(graph = sub_graph, filename = "format_agent_subgraph.png")
