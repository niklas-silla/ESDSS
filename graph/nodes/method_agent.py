from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.method_tools import create_vectorstore, method_analysis, method_report_agent
from langgraph.graph import StateGraph, START, END
import time

AGENT = "method_agent"

def method_check_node(state: AgentState) -> AgentState:
    """
    Node to check the researchquestion and methodology used in the manuscript.
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
def create_vectorstore_node(state: AgentState):
    state[AGENT]["data"]["vectorstore"] = create_vectorstore(state["md_manuscript_path"])
    return state

def analyze_method_node(state: AgentState):
    state[AGENT]["data"]["context"] = method_analysis(state[AGENT]["data"]["vectorstore"])

def method_report_node(state: AgentState):
    report, input_tokens, output_tokens = method_report_agent(state[AGENT]["data"]["context"])
    state[AGENT]["data"].update(report)
    state[AGENT]["input_tokens"] = input_tokens
    state[AGENT]["output_tokens"] = output_tokens
    return state

# -----------
#  Sub Graph
# -----------
method_graph = StateGraph(AgentState)
method_graph.add_node("create_vectorstore", create_vectorstore_node)
method_graph.add_node("analyze_method", analyze_method_node)
method_graph.add_node("generate_report", method_report_node)

method_graph.add_edge(START, "create_vectorstore")
method_graph.add_edge("create_vectorstore", "analyze_method")
method_graph.add_edge("analyze_method", "generate_report")
method_graph.add_edge("generate_report", END)

sub_graph = method_graph.compile()
#visualize_graph_png(graph = sub_graph, filename = "method_agent_subgraph.png")
