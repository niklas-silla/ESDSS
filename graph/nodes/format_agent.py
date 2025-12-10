from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.format_tools import formatting_check, section_check, format_report_agent
from langgraph.graph import StateGraph, START, END
import time

AGENT = "format_agent"

def format_check_node(state: AgentState) -> AgentState:
    """
    Node to check the format of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
    try:
        start_sub_graph = time.perf_counter()
        state = sub_graph.invoke(state)
        end_sub_graph = time.perf_counter()
        state[AGENT]["duration"] = end_sub_graph - start_sub_graph
        state[AGENT]["status"]= "success"
    except Exception as e:
        state[AGENT]["status"]= "failed"
        state[AGENT]["error"].append(e)
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def section_check_node(state: AgentState):
    result, input_tokens, output_tokens = section_check(state["md_manuscript_path"])
    state[AGENT]["data"]["section_check"] = result
    state[AGENT]["input_tokens"] = input_tokens
    state[AGENT]["output_tokens"] = output_tokens
    return state

def formatting_check_node(state: AgentState):
    state[AGENT]["data"]["formatting_check"] = formatting_check(state["preprocessed_manuscript_path"], state["md_manuscript_path"])
    return state

def format_report_node(state: AgentState):
    report, input_tokens, output_tokens = format_report_agent(state[AGENT]["data"]["formatting_check"], state[AGENT]["data"]["section_check"])
    state[AGENT]["data"].update(report)
    state[AGENT]["input_tokens"] += input_tokens
    state[AGENT]["output_tokens"] += output_tokens
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
#visualize_graph_png(graph = sub_graph, filename = "format_agent_subgraph.png")
