from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.scopefit_tools import extract_manuscript_data, calculate_cosine_similarity, generate_scopefit_report
from langgraph.graph import StateGraph, START, END
import time

AGENT = "scopefit_agent"

def scope_fit_node(state: AgentState) -> AgentState:
    """
    Node to check the scope fit of a PDF manuscript.
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
        state[AGENT]["error"].append(str(e)) # str() otherwise not JSON serializable
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def manuscript_extract_node(state: AgentState):
    state[AGENT]["data"]["manuscript_data"] = extract_manuscript_data(state["original_manuscript_path"])
    return state

def cosine_similarity_calculator_node(state: AgentState):
    calculations = calculate_cosine_similarity(state[AGENT]["data"]["manuscript_data"])
    state[AGENT]["data"].update(calculations)
    return state

def report_node(state: AgentState):
    report, input_tokens, output_tokens = generate_scopefit_report(
        state[AGENT]["data"]["manuscript_data"],
        state[AGENT]["data"]["neighbor_info"],
        state[AGENT]["data"]["title_cs_median"],
        state[AGENT]["data"]["abstract_cs_median"]
    )
    state[AGENT]["data"].update(report)
    state[AGENT]["input_tokens"] = input_tokens
    state[AGENT]["output_tokens"] = output_tokens
    return state

# -----------
#  Sub Graph
# -----------
scopefit_graph = StateGraph(AgentState)
scopefit_graph.add_node("extract_title_abstract", manuscript_extract_node)
scopefit_graph.add_node("calculate_cosine_similarity", cosine_similarity_calculator_node)
scopefit_graph.add_node("generate_report", report_node)

scopefit_graph.add_edge(START, "extract_title_abstract")
scopefit_graph.add_edge("extract_title_abstract", "calculate_cosine_similarity")
scopefit_graph.add_edge("calculate_cosine_similarity", "generate_report")
scopefit_graph.add_edge("generate_report", END)

sub_graph = scopefit_graph.compile()
#visualize_graph_png(graph = sub_graph, filename = "scopefit_agent_subgraph.png")
