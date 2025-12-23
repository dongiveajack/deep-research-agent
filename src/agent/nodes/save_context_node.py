from typing import Any

from src.agent.states.agent_state import AgentState
from src.agent.utils.memory import save_summary


def save_context_node(state: AgentState) -> dict[str, Any]:
    """Generate a description and save the research into memory."""
    topic = state["topic"]
    summary = state["final_summary"]
    # description = state["summary_description"]

    # Save to Vector DB and JSON Index
    save_summary(topic, summary, "")

    return {}
