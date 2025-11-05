from graph.state import AgentState

def plagiarism_detection_node(state: AgentState) -> AgentState:
    """
    Node to detect plagiarism aspects of a PDF manuscript.
    """
    
    agent_name="plagiarism_agent"
    state[agent_name]["status"]= "running"
    print("Plagiarism detection Agent runs ...")
    
    # Simulate innovation checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]