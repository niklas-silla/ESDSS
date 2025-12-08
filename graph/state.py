from typing import TypedDict, Optional, List

class AgentResult(TypedDict):
    status: str # "pending", "running", "success", "failed"
    data: dict
    error: List[str]
    retries: int

# State schema
class AgentState(TypedDict):
    original_manuscript_path: str
    preprocessed_manuscript_path: str
    md_manuscript_path: str
    images: list[str]
    artifacts_folder: str
    message: str

    # orchestrator
    workflow_step: int
    success_logged: set[str]  # Tracking which Agents have already been logged
    next_node: list[str]  # To handle dynamic next nodes

    # agents
    preprocessing_agent: AgentResult
    format_agent: AgentResult
    innovation_agent: AgentResult
    method_agent: AgentResult
    plagiarism_agent: AgentResult
    quality_agent: AgentResult
    scopefit_agent: AgentResult
    report_agent: AgentResult

    # final decision
    deskreject: bool
    final_report: str


def create_initial_state(original_manuscript_path: str, artifacts_folder: str) -> AgentState:
    """
    Create new AgentState with default values.
    """
    
    return {
        "original_manuscript_path": original_manuscript_path,
        "preprocessed_manuscript_path": None,
        "md_manuscript_path": None,
        "images": [],
        "artifacts_folder": artifacts_folder,
        "message": "",
        "workflow_step": 0,
        "success_logged": set(),
        "next_node": [],
        "preprocessing_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "format_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "innovation_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "method_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "plagiarism_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "quality_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "scopefit_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "report_agent": {
            "status": "pending",
            "data": {},
            "error": [],
            "retries": 0
        },
        "deskreject": None,
        "final_report": None,
    }