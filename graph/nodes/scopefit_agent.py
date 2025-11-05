from graph.state import AgentState

def scope_fit_node(state: AgentState) -> AgentState:
    """
    Node to check the scope fit of a PDF manuscript.
    """

    agent_name="scopefit_agent"
    state[agent_name]["status"]= "running"
    print("Scope fit Agent runs ...")
    
    # Simulate format checking logic here
    
    state[agent_name]["status"]= "success"
    return state[agent_name]