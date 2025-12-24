from typing import Any

from langgraph.runtime import Runtime
from langgraph.store.base import SearchItem

from src.agent.states.agent_state import AgentState, TempState
from src.agent.utils.memory import save_to_vector_db


def save_context_node(state: AgentState, runtime: Runtime) -> dict[str, Any]:
    """Generate a description and save the research into memory."""
    topic = state["final_topic"]
    summary = state["final_summary"]
    memory_summary = state["memory_summary"]

    # Save to Vector DB and JSON Index
    save_to_vector_db(topic, summary)

    # save to long term memory
    memory = runtime.store
    memory.put(
        namespace=("research",),
        key=topic,
        value={
            "summary": memory_summary
        }
    )

    return {}


def save_long_term_memory(state: TempState, runtime: Runtime) -> dict[str, Any]:
    memory = runtime.store
    memory.put(
        namespace=("research",),
        key=state['first_name'],
        value={
            'first_name': state['first_name'],
            "last_name": state['last_name'],
        }
    )

    return {
        "finished": True
    }


def get_long_term_memory(state: TempState, runtime: Runtime) -> dict[str, Any]:
    print("searching long term memory for query - abhinav tripathi")
    memory: list[SearchItem] = runtime.store.search(("research",), query="cian agro analysis")
    data = "\n".join(f"Memory retrieved {item.key} -> {item.value}" for item in memory)
    return {
        'result': data
    }
