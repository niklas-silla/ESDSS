from graph.state import AgentState

def innovation_check_node(state: AgentState) -> AgentState:
    """
    Node to check the innovation aspects of a PDF manuscript.
    """

    agent_name="innovation_agent"
    state[agent_name]["status"]= "running"
    print("Innovation check Agent runs ...")
    
    # Simulate innovation checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]