from graph.state import AgentState

def quality_check_node(state: AgentState) -> AgentState:
    """
    Node to check the quality aspects of a PDF manuscript.
    """

    agent_name="quality_agent"
    state[agent_name]["status"]= "running"
    print("Quality check Agent runs ...")
    
    # Simulate format checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]