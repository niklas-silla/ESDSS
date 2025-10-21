from typing import TypedDict

# The state schema
class AgentState(TypedDict):
    md_document: str
    number_of_tables: int
    number_of_pictures: int
    images: list[str]
    message: str