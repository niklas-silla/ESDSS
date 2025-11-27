from graph.state import AgentState
from graph.tools.scopefit_tools import extract_manuscript_data, calculate_cosine_similarity, generate_scopefit_report
from langgraph.graph import StateGraph, START, END

AGENT = "scopefit_agent"

def scope_fit_node(state: AgentState) -> AgentState:
    """
    Node to check the scope fit of a PDF manuscript.
    """
    state[AGENT]["status"]= "running"

    state = sub_graph.invoke(state)
    
    state[AGENT]["status"]= "success"
    return state[AGENT]


# -----------
#  Sub Nodes
# -----------
def manuscript_extract_node(state: AgentState):
    state[AGENT]["data"]["manuscript_data"] = extract_manuscript_data(state["manuscript_path"])
    return state

def cosine_similarity_calculator_node(state: AgentState):
    calculations = calculate_cosine_similarity(state[AGENT]["data"]["manuscript_data"])
    state[AGENT]["data"].update(calculations)
    return state

def report_node(state: AgentState):
    report = generate_scopefit_report(
        state[AGENT]["data"]["manuscript_data"],
        state[AGENT]["data"]["neighbor_info"],
        state[AGENT]["data"]["title_cs_median"],
        state[AGENT]["data"]["abstract_cs_median"]
    )
    state[AGENT]["data"].update(report)
    return state

# -----------
#  Sub Graph
# -----------
quality_graph = StateGraph(AgentState)
quality_graph.add_node("extractor", manuscript_extract_node)
quality_graph.add_node("cs_calculator", cosine_similarity_calculator_node)
quality_graph.add_node("report", report_node)

quality_graph.add_edge(START, "extractor")
quality_graph.add_edge("extractor", "cs_calculator")
quality_graph.add_edge("cs_calculator", "report")
quality_graph.add_edge("report", END)

sub_graph = quality_graph.compile()
