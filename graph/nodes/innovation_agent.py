from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.innovation_tools import extract_innovation_statement, search_semantic_scholar, search_arxiv, innovation_report_agent
from langgraph.graph import StateGraph, START, END
import time

AGENT = "innovation_agent"

def innovation_check_node(state: AgentState) -> AgentState:
    """
    Node to check the innovation aspects of a PDF manuscript.
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
def extract_innovation_node(state: AgentState):
    result, input_tokens, output_tokens = extract_innovation_statement(state["md_manuscript_path"])
    state[AGENT]["data"] = result
    state[AGENT]["input_tokens"] = input_tokens
    state[AGENT]["output_tokens"] = output_tokens
    return state

def semantic_scholar_node(state: AgentState):
    state[AGENT]["data"]["semantic_scholar_results"] = search_semantic_scholar(state[AGENT]["data"]["search_queries"])
    return state

def arxiv_node(state: AgentState):
    state[AGENT]["data"]["arxiv_results"] = search_arxiv(state[AGENT]["data"]["search_queries"])
    return state

def innovation_report_node(state: AgentState):
    report, input_tokens, output_tokens = innovation_report_agent(state[AGENT]["data"]["innovation_statement"], state[AGENT]["data"]["semantic_scholar_results"], state[AGENT]["data"]["arxiv_results"])
    state[AGENT]["data"].update(report)
    state[AGENT]["input_tokens"] += input_tokens
    state[AGENT]["output_tokens"] += output_tokens
    return state

# -----------
#  Sub Graph
# -----------
innovation_graph = StateGraph(AgentState)
innovation_graph.add_node("extract_innovation", extract_innovation_node)
innovation_graph.add_node("search_semantic_scholar", semantic_scholar_node)
innovation_graph.add_node("search_arxiv", arxiv_node)
innovation_graph.add_node("generate_report", innovation_report_node)

innovation_graph.add_edge(START, "extract_innovation")
innovation_graph.add_edge("extract_innovation", "search_semantic_scholar")
innovation_graph.add_edge("search_semantic_scholar", "search_arxiv")
innovation_graph.add_edge("search_arxiv", "generate_report")
innovation_graph.add_edge("generate_report", END)

sub_graph = innovation_graph.compile()
#visualize_graph_png(graph = sub_graph, filename = "innovation_agent_subgraph.png")
