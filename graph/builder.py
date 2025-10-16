from langgraph.graph import StateGraph, START, END
from graph.nodes.docling import greeting_node
from graph.state import AgentState

# build a graph
def build_graph():
    graph = StateGraph(AgentState)


    # add nodes
    graph.add_node("greeter", greeting_node)

    # startpoint
    graph.add_edge(START, "greeter")

    # edges & conditions
    # graph.add_edge("", "")

    # endpoint
    graph.add_edge("greeter", END)

    return graph