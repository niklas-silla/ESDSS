from langgraph.graph import StateGraph, START, END
from graph.nodes.docling import docling_node
from graph.state import AgentState

# build a graph
def build_graph():
    graph = StateGraph(AgentState)


    # add nodes
    graph.add_node("docling", docling_node)

    # startpoint
    graph.add_edge(START, "docling")

    # edges & conditions
    # graph.add_edge("", "")

    # endpoint
    graph.add_edge("docling", END)

    return graph