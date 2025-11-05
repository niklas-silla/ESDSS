from langgraph.graph import StateGraph, START, END
from graph.nodes.preprocessing import manuscript_preprocessing_node
from graph.nodes.orchestrator import orchestrator_node, orchestrator_decision
from graph.nodes.format_agent import format_check_node
from graph.nodes.innovation_agent import innovation_check_node
from graph.nodes.method_agent import method_check_node 
from graph.nodes.plagiarism_agent import plagiarism_detection_node
from graph.nodes.quality_agent import quality_check_node
from graph.nodes.scopefit_agent import scope_fit_node
from graph.nodes.report_agent import report_generator_node
from graph.state import AgentState

def build_graph():
    graph = StateGraph(AgentState)

    # add nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("preprocessing", manuscript_preprocessing_node)
    graph.add_node("format_agent", format_check_node)
    graph.add_node("innovation_agent", innovation_check_node)
    graph.add_node("method_agent", method_check_node)
    graph.add_node("plagiarism_agent", plagiarism_detection_node)
    graph.add_node("quality_agent", quality_check_node)
    graph.add_node("scopefit_agent", scope_fit_node)
    graph.add_node("report_agent", report_generator_node)

    # startpoint
    graph.add_edge(START, "orchestrator")

    # edges
    graph.add_conditional_edges(
        "orchestrator", # source
        orchestrator_decision, # path
        {
            # Edge: Node
            "preprocessing": "preprocessing",
            "format_agent": "format_agent",
            "innovation_agent": "innovation_agent",
            "method_agent": "method_agent",
            "plagiarism_agent": "plagiarism_agent",
            "quality_agent": "quality_agent",
            "scopefit_agent": "scopefit_agent",
            "report_agent": "report_agent",
            "orchestrator": "orchestrator",
            END: END    
        }
    )
    # all worker agents report to orchestrator
    for agent in ["preprocessing", "format_agent", "innovation_agent", "method_agent", "plagiarism_agent", "quality_agent", "scopefit_agent", "report_agent"]:
        graph.add_edge(agent, "orchestrator")

    # endpoint
    graph.add_edge("orchestrator", END)

    return graph