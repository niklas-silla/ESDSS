from graph.state import AgentState
from graph.visualizer import visualize_graph_png
from graph.tools.preprocessing_tools import preprocessing, docling_converter
from langgraph.graph import StateGraph, START, END
from pathlib import Path
import fitz  # PyMuPDF library for PDF processing


AGENT = "preprocessing_agent"

def manuscript_preprocessing_node(state: AgentState) -> AgentState:
    """
    Node to preprocess a PDF manuscript.
    """
    state[AGENT]["status"]= "running"
    try:
        state = sub_graph.invoke(state)
        state[AGENT]["status"]= "success"
    except Exception as e:
        state[AGENT]["status"]= "failed"
        state[AGENT]["error"].append(e)
    return state


# -----------
#  Sub Nodes
# -----------
def preprocessing_node(state: AgentState):
    state["preprocessed_manuscript_path"] = preprocessing(Path(state["original_manuscript_path"]), Path(state["artifacts_folder"]))
    return state

def docling_node(state: AgentState):
    result = docling_converter(Path(state["preprocessed_manuscript_path"]), Path(state["artifacts_folder"]))

    state["md_manuscript_path"] = str(result["md_manuscript_path"])
    state[AGENT]["data"]["number_of_tables"] = result["number_of_tables"]
    state[AGENT]["data"]["number_of_pictures"] = result["number_of_pictures"]
    state["images"] = result["images"]
    return state

# -----------
#  Sub Graph
# -----------
preprocessing_graph = StateGraph(AgentState)
preprocessing_graph.add_node("preprocessing", preprocessing_node)
preprocessing_graph.add_node("run_docling", docling_node)

preprocessing_graph.add_edge(START, "preprocessing")
preprocessing_graph.add_edge("preprocessing", "run_docling")
preprocessing_graph.add_edge("run_docling", END)

sub_graph = preprocessing_graph.compile()
#visualize_graph_png(graph = sub_graph, filename = "preprocessing_subgraph.png")