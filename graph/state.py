from typing import TypedDict

# The state schema
class AgentState(TypedDict):
    manuscript_path: str
    md_manuscript_path: str
    number_of_tables: int
    number_of_pictures: int
    images: list[str]
    message: str