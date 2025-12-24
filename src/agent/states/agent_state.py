from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    topic: str
    generated_queries: list[str]
    past_queries: Annotated[list[str], operator.add]
    source_documents: Annotated[list[dict[str, str]], operator.add]
    final_topic: str
    final_summary: str
    memory_summary: str
    memory_context: str
    use_memory: bool
    start_research: bool
    evaluation_result: bool

class TempState(TypedDict):
    first_name: str
    last_name: str
    finished: bool
    result: str
