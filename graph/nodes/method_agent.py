from graph.state import AgentState
from graph.tools.method_tools import create_vectorstore, method_analysis
from langgraph.graph import StateGraph, START, END

AGENT = "method_agent"

def method_check_node(state: AgentState) -> AgentState:
    """
    Node to check the researchquestion and methodology used in the manuscript.
    """
    state[AGENT]["status"]= "running"
    
    state = sub_graph.invoke(state)
    
    state[AGENT]["status"]= "success"
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def create_vectorstore_node(state: AgentState):
    state[AGENT]["data"]["vectorstore"] = create_vectorstore(state["md_manuscript_path"])
    return state

def method_analysis_node(state: AgentState):
    report = method_analysis(state[AGENT]["data"]["vectorstore"])
    state[AGENT]["data"].update(report)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("create_vectorstore_node", create_vectorstore_node)
quality_graph.add_node("method_analysis_node", method_analysis_node)


quality_graph.add_edge(START, "create_vectorstore_node")
quality_graph.add_edge("create_vectorstore_node", "method_analysis_node")
quality_graph.add_edge("method_analysis_node", END)

sub_graph = quality_graph.compile()
