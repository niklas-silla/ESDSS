from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.innovation_tools import extract_innovation_statement, search_semantic_scholar, search_arxiv, innovation_report_agent
from langgraph.graph import StateGraph, START, END

AGENT = "innovation_agent"

def innovation_check_node(state: AgentState) -> AgentState:
    """
    Node to check the innovation aspects of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
    
    state = sub_graph.invoke(state)
    
    state[AGENT]["status"]= "success"
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def extract_innovation_node(state: AgentState):
    state[AGENT]["data"] = extract_innovation_statement(state["md_manuscript_path"])
    return state

def semantic_scholar_node(state: AgentState):
    state[AGENT]["data"]["semantic_scholar_results"] = search_semantic_scholar(state[AGENT]["data"]["search_queries"])
    return state

def arxiv_node(state: AgentState):
    state[AGENT]["data"]["arxiv_results"] = search_arxiv(state[AGENT]["data"]["search_queries"])
    return state

def innovation_report_node(state: AgentState):
    report = innovation_report_agent(state[AGENT]["data"]["innovation_statement"], state[AGENT]["data"]["semantic_scholar_results"], state[AGENT]["data"]["arxiv_results"])
    state[AGENT]["data"].update(report)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("extract_innovation", extract_innovation_node)
quality_graph.add_node("semantic_scholar", semantic_scholar_node)
quality_graph.add_node("arxiv", arxiv_node)
quality_graph.add_node("report", innovation_report_node)

quality_graph.add_edge(START, "extract_innovation")
quality_graph.add_edge("extract_innovation", "semantic_scholar")
quality_graph.add_edge("semantic_scholar", "arxiv")
quality_graph.add_edge("arxiv", "report")
quality_graph.add_edge("report", END)

sub_graph = quality_graph.compile()
visualize_graph_png(graph = sub_graph, filename = "innovation_agent_subgraph.png")
