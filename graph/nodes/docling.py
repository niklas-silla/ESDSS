from graph.state import AgentState

# only a test node
def greeting_node(state: AgentState) -> AgentState:
    """
    Simple node that adds a greeting message to the state.
    """

    state['message'] = "Hey " + state["message"] + ", how is your day going?"

    return state