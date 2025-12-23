from typing import Any

from src.agent.chains.memory_router import memory_router_chain
from src.agent.states.agent_state import AgentState
from src.agent.utils.memory import get_research_index


def router_node(state: AgentState) -> dict[str, Any]:
    """Decide if we should search the vector database."""
    research_index = get_research_index()
    if not research_index:
        return {"use_memory": False, "memory_context": ""}

    result = memory_router_chain().invoke({
        "user_query": state["topic"],
        "research_index": str(research_index)
    })

    return {
        "use_memory": result.use_memory,
        "summary_description": "",
        "generated_queries": [],
        "past_queries": [],
        "source_documents": [],
        "final_summary": "",
        "memory_context": ""
    }
