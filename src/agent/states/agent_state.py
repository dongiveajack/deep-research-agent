from typing import TypedDict


class AgentState(TypedDict):
    topic: str
    generated_queries: list[str]
    past_queries: list[str]
    source_documents: list[dict[str, str]]
    final_summary: str
    evaluation_result: bool
    start_research: bool