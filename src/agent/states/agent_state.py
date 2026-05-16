from typing import TypedDict, Annotated, Union
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
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
    next_node: str # Added to track routing from supervisor

class TempState(TypedDict):
    first_name: str
    last_name: str
    finished: bool
    result: str
