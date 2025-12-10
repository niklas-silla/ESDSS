import csv

def create_evaluation_csv(path):
    with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                            # workflow data
                            "m_id", 
                            "deskreject", 
                            "workflow_success", 
                            "total_duration",
                            "total_input_tokens",
                            "total_output_tokens",
                            # preprocessing agent data
                            "preprocessing_agent_status",
                            "preprocessing_agent_retries",
                            "preprocessing_agent_duration",
                            # scopefit agent data
                            "scopefit_agent_status",
                            "scopefit_agent_retries",
                            "scopefit_agent_duration",
                            "scopefit_agent_input_tokens",
                            "scopefit_agent_output_tokens",
                            # method agent data
                            "method_agent_status",
                            "method_agent_retries",
                            "method_agent_duration",
                            "method_agent_input_tokens",
                            "method_agent_output_tokens",
                            # innovation agent data
                            "innovation_agent_status",
                            "innovation_agent_retries",
                            "innovation_agent_duration",
                            "innovation_agent_input_tokens",
                            "innovation_agent_output_tokens",
                            # format agent data
                            "format_agent_status",
                            "format_agent_retries",
                            "format_agent_duration",
                            "format_agent_input_tokens",
                            "format_agent_output_tokens",
                            # quality agent data
                            "quality_agent_status",
                            "quality_agent_retries",
                            "quality_agent_duration",
                            "quality_agent_input_tokens",
                            "quality_agent_output_tokens",
                            # report agent data
                            "report_agent_status",
                            "report_agent_retries",
                            "report_agent_duration",
                            "report_agent_input_tokens",
                            "report_agent_output_tokens",
                            # final report
                            "final_report"
                            ])  # column headings
            
            

def prepare_csv_row(m_id: str, state) -> list:
      total_input_tokens = sum([state["scopefit_agent"]["input_tokens"], 
                               state["method_agent"]["input_tokens"],
                               state["innovation_agent"]["input_tokens"],
                               state["format_agent"]["input_tokens"],
                               state["quality_agent"]["input_tokens"],
                               state["report_agent"]["input_tokens"]])
      total_output_tokens = sum([state["scopefit_agent"]["output_tokens"], 
                               state["method_agent"]["output_tokens"],
                               state["innovation_agent"]["output_tokens"],
                               state["format_agent"]["output_tokens"],
                               state["quality_agent"]["output_tokens"],
                               state["report_agent"]["output_tokens"]])
      row = [
            # workflow data
            m_id, 
            state["deskreject"], 
            state["workflow_success"], 
            state["total_duration"], 
            total_input_tokens,
            total_output_tokens, 
            # preprocessing agent data
            state["preprocessing_agent"]["status"],
            state["preprocessing_agent"]["retries"],
            state["preprocessing_agent"]["duration"],
            # scopefit agent data
            state["scopefit_agent"]["status"],
            state["scopefit_agent"]["retries"],
            state["scopefit_agent"]["duration"],
            state["scopefit_agent"]["input_tokens"],
            state["scopefit_agent"]["output_tokens"],
            # method agent data
            state["method_agent"]["status"],
            state["method_agent"]["retries"],
            state["method_agent"]["duration"],
            state["method_agent"]["input_tokens"],
            state["method_agent"]["output_tokens"],
            # innovation agent data
            state["innovation_agent"]["status"],
            state["innovation_agent"]["retries"],
            state["innovation_agent"]["duration"],
            state["innovation_agent"]["input_tokens"],
            state["innovation_agent"]["output_tokens"],
            # format agent data
            state["format_agent"]["status"],
            state["format_agent"]["retries"],
            state["format_agent"]["duration"],
            state["format_agent"]["input_tokens"],
            state["format_agent"]["output_tokens"],
            # quality agent data
            state["quality_agent"]["status"],
            state["quality_agent"]["retries"],
            state["quality_agent"]["duration"],
            state["quality_agent"]["input_tokens"],
            state["quality_agent"]["output_tokens"],
            # report agent data
            state["report_agent"]["status"],
            state["report_agent"]["retries"],
            state["report_agent"]["duration"],
            state["report_agent"]["input_tokens"],
            state["report_agent"]["output_tokens"],
            # final report
            state["final_report"], 
            ]
      return row

def save_row_in_csv(path, row):
      with open(path, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)