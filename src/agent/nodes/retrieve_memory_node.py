from typing import Any
from src.agent.states.agent_state import AgentState
from src.agent.utils.memory import retrieve_context


def retrieve_memory_node(state: AgentState) -> dict[str, Any]:
    """Retrieve context from vector database if router decided it's needed."""
    if not state.get("use_memory"):
        return {"memory_context": ""}

    context = retrieve_context(state["topic"])
    return {"memory_context": context}
