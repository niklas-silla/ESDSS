from graph.state import AgentState
from langgraph.graph import END

def orchestrator_node(state: AgentState) -> AgentState:
    """
    Node to orchestrate the worker agents.
    """
    # Set agent names
    preprocessing_agent ="preprocessing_agent" 
    criterion_agents = ["format_agent", "innovation_agent", "method_agent", "plagiarism_agent", "quality_agent", "scopefit_agent"]
    report_agent = "report_agent"


    ############
    # WORKFLOW #
    ############
    
    # STEP 0: Start preprocessing
    if state["workflow_step"] == 0:
        print("🔄 preprocessing started ...")
        state["workflow_step"] += 1
        state["message"] = "Starting preprocessing of the manuscript."
        state["next_node"] = [preprocessing_agent]
        return state
    
    # STEP 1: Check preprocessing & decide next step
    if state["workflow_step"] == 1:
        # Check if preprocessing is done
        status = state[preprocessing_agent]["status"]
        retries = state[preprocessing_agent]["retries"]

        if status == "success" and state["md_manuscript_path"] is not None:
            print("✅ preprocessing completed successfully")
            print("🔄 criteria agents started...")
            state["workflow_step"] += 1
            state["message"] = "Preprocessing completed successfully. Proceeding to criterion checks."
            state["next_node"] = criterion_agents
            return state
        elif status == "failed" and retries < 2:
            print(f"⚠️ preprocessing failed, retrying (attempt {retries + 1}/{2})...")
            state[preprocessing_agent]["retries"] += 1
            state["message"] = f"Preprocessing failed. Retrying preprocessing (Attempt {retries + 1})."
            state["next_node"] = [preprocessing_agent]
            return state
        else:
            print("❌ preprocessing failed. STOPPED")
            state["message"] = "Preprocessing failed after multiple attempts. Workflow stopped."
            state["next_node"] = [END]
            return state  # End workflow
    
    # STEP 2: Check criterion agents results 
    if state["workflow_step"] == 2:
        all_finished = True # Assumption is True -> can be set to False during iteration via agents 
        any_failed = False # Assumption is False -> can be set to True if an agent permanently failed
        for agent in criterion_agents:
            status = state[agent]["status"]

            if status == "running":
                print(f"⏳ {agent} is still running...")
                all_finished = False

            elif status == "success":
                if agent not in state["finished_logged"]:
                    print(f"✅ {agent} completed successfully")
                    state["finished_logged"].add(agent)

            elif status == "failed":
                retries = state[agent]["retries"]
                error = str(state[agent]["error"]) # List -> str 
                
                if retries < 2:
                    state[agent]["retries"] += 1
                    print(f"⚠️ {agent} failed, retrying (attempt {retries + 1}/{2})...")
                    
                    all_finished = False
                    state["next_node"] = [agent]
                    return state  # Retry the failed agent

                else:
                    print(f"❌ {agent} failed permanently. STOPPED")
                    print(f"Error of {agent}: {error}")
                    any_failed = True
                    state["finished_logged"].add(agent)

        if all_finished:
            if not any_failed:
                print("\n🎉 All worker agents completed successfully!")
                state["message"] = "All workers completed successfully"
            else:
                print("\n⚠️ Some agents failed permanently. Workflow continues to reporting.")
                state["message"] = "All workers completed but some failed"
            
            state["workflow_step"] += 1
            print("🔄 report generation started...")
            state["next_node"] = [report_agent]
            return state
        
        else:
            # Noch Agents am Laufen - weiter warten
            print(f"\n⏸️ Waiting for {sum(1 for a in criterion_agents if state[a]['status'] == 'running')} agents to complete...")
            state["message"] = "Workers in progress"
            state["next_node"] = ["orchestrator"]
            return state # Stay in orchestrator to check again later
        
    # STEP 3: Check report agent result
    if state["workflow_step"] == 3:
        # Check if reporting is done
        status = state[report_agent]["status"]
        retries = state[report_agent]["retries"]

        if status == "success":
            print("✅ report generated successfully.")
            state["workflow_step"] += 1
            state["message"] = "Report successfully generated. Workflow completed."
            # set workflow as success
            state["workflow_success"] = True
            state["next_node"] = [END]
            return state  # End workflow
        elif status == "failed" and retries < 2:
            print(f"⚠️ report generation failed, retrying (attempt {retries + 1}/{2})...")
            state[report_agent]["retries"] += 1
            state["message"] = f"Report generation failed. Retrying report generation (Attempt {retries + 1})."
            state["next_node"] = [report_agent]
            return state
        else:
            print("❌ report generation failed permanently. STOPPED")
            state["message"] = "Report generation failed after multiple attempts. Workflow stopped."
            state["next_node"] = [END]
            return state  # End workflow

    state["next_node"] = ["orchestrator"]
    return state  # Stay in orchestrator to check again later


def orchestrator_decision(state: AgentState) -> list[str]:
    """
    Decision function for the orchestrator node to determine the next nodes to invoke.
    """
    return state["next_node"]