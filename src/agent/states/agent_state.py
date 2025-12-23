from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    topic: str
    summary_description: str
    generated_queries: list[str]
    past_queries: Annotated[list[str], operator.add]
    source_documents: Annotated[list[dict[str, str]], operator.add]
    final_summary: str
    memory_context: str
    use_memory: bool
    start_research: bool
    evaluation_result: bool
