from graph.state import AgentState

def method_check_node(state: AgentState) -> AgentState:
    """
    Node to check the methods used in a PDF manuscript.
    """
    
    agent_name="method_agent"
    state[agent_name]["status"]= "running"
    print("Method check Agent runs ...")
    
    # Simulate innovation checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]