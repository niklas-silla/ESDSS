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
format_graph = StateGraph(AgentState)
format_graph.add_node("check_section", section_check_node)
format_graph.add_node("check_formatting", formatting_check_node)
format_graph.add_node("generate_report", format_report_node)

format_graph.add_edge(START, "check_section")
format_graph.add_edge("check_section", "check_formatting")
format_graph.add_edge("check_formatting", "generate_report")
format_graph.add_edge("generate_report", END)

sub_graph = format_graph.compile()
visualize_graph_png(graph = sub_graph, filename = "format_agent_subgraph.png")
