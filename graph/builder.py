from langgraph.graph import StateGraph, START, END
from graph.nodes.preprocessing import manuscript_preprocessing_node
from graph.state import AgentState

# build a graph
def build_graph():
    graph = StateGraph(AgentState)

    # add nodes
    graph.add_node("preprocessing", manuscript_preprocessing_node)

    # startpoint
    graph.add_edge(START, "preprocessing")

    # edges & conditions
    # graph.add_edge("", "")

    # endpoint
    graph.add_edge("preprocessing", END)

    return graph