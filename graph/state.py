from typing import TypedDict, Optional

class AgentResult(TypedDict):
    status: str # "pending", "running", "success", "failed"
    data: dict
    error: Optional[str]
    retries: int

# The state schema
class AgentState(TypedDict):
    manuscript_path: str
    preprocessed_manuscript_path: str
    md_manuscript_path: str
    md_report_path: str
    number_of_tables: int
    number_of_pictures: int
    images: list[str]
    message: str
    workflow_step: int
    success_logged: set[str]  # Tracking which Agents have already been logged
    next_node: list[str]  # To handle dynamic next nodes
    preprocessing: AgentResult
    format_agent: AgentResult
    innovation_agent: AgentResult
    method_agent: AgentResult
    plagiarism_agent: AgentResult
    quality_agent: AgentResult
    scopefit_agent: AgentResult
    report_agent: AgentResult


def create_initial_state(manuscript_path: str) -> AgentState:
    """Create new AgentState with default values."""
    return {
        "manuscript_path": manuscript_path,
        "preprocessed_manuscript_path": None,
        "md_manuscript_path": None,
        "md_report_path": None,
        "number_of_tables": 0,
        "number_of_pictures": 0,
        "images": [],
        "message": "",
        "workflow_step": 0,
        "success_logged": set(),
        "next_node": [],
        "preprocessing": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "format_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "innovation_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "method_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "plagiarism_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "quality_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "scopefit_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
        "report_agent": {
            "status": "pending",
            "data": {},
            "error": None,
            "retries": 0
        },
    }