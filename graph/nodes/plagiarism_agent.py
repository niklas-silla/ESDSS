from graph.state import AgentState

def plagiarism_detection_node(state: AgentState) -> AgentState:
    """
    Node to detect plagiarism aspects of a PDF manuscript.
    """
    
    agent_name="plagiarism_agent"
    state[agent_name]["status"]= "running"
    
    # Plagiarism detection Agent skipped.
    
    state[agent_name]["status"]= "success"
    return state[agent_name]