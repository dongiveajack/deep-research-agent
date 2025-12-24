from typing import Any

from langgraph.runtime import Runtime
from langgraph.store.base import SearchItem

from src.agent.chains.memory_router import memory_router_chain
from src.agent.states.agent_state import AgentState


def router_node(state: AgentState, runtime: Runtime) -> dict[str, Any]:
    """check in long-term memory if the agent has already researched on this topic before"""
    memory_store = runtime.store
    memory: list[SearchItem] = memory_store.search(("research",), query=state['topic'])
    data = "\n".join(f"topic: {item.key} summary: {item.value.get('summary')}" for item in memory)

    result = memory_router_chain().invoke({
        "user_query": state["topic"],
        "long_term_memory": data
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
