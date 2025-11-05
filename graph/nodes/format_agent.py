from graph.state import AgentState


def format_check_node(state: AgentState) -> AgentState:
    """
    Node to check the format of a PDF manuscript.
    """
    agent_name="format_agent"
    state[agent_name]["status"]= "running"
    print("Format check Agent runs ...")
    
    # Simulate format checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]