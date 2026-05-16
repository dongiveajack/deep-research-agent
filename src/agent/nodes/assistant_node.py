from typing import Any
from langchain_core.messages import HumanMessage, AIMessage
from src.agent.chains.assistant_chain import assistant_chain
from src.agent.states.agent_state import AgentState


def assistant_node(state: AgentState) -> dict[str, Any]:
    """Decide between conversation and research, and respond directly if it's a chat."""
    messages = state.get("messages", [])
    
    # If messages is empty but topic is provided (old format), create a message
    if not messages and state.get("topic"):
        messages = [HumanMessage(content=state["topic"])]
    
    if not messages:
        return {"next_node": "conversation", "topic": ""}

    result = assistant_chain().invoke({"messages": messages})
    
    updates = {
        "messages": messages if not state.get("messages") else []
    }

    if result.is_research:
        updates["next_node"] = "research"
        updates["topic"] = result.topic
        updates["final_summary"] = "" # Clear previous summary to avoid ghost messages
    else:
        updates["next_node"] = "conversation"
        updates["messages"].append(AIMessage(content=result.response))
        updates["final_summary"] = result.response # For frontend display

    return updates
