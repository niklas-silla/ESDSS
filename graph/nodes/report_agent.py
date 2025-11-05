from graph.state import AgentState

def report_generator_node(state: AgentState) -> AgentState:
    """
    Node to generate a report from all the agent analysis of a PDF manuscript.
    """
    
    agent_name="report_agent"
    state[agent_name]["status"]= "running"
    print("Report generator Agent runs ...")
    
    # Simulate format checking logic here
    
    state["md_report_path"]= ""
    state[agent_name]["status"]= "success"
    
    return state