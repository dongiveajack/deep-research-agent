from typing import List, Dict, Any

from src.agent.states.agent_state import AgentState
from src.agent.chains.summarize_sources import summarize_sources_chain
from src.agent.utils.common import format_sources_for_llm


def summarization_sources(state: AgentState):
    """Uses LLM to summarize the findings from web search related to the user-provided research topic"""
    topic = state['topic']
    sources = state['source_documents']

    result = summarize_sources_chain().invoke({
        'topic': topic,
        'source_documents': format_sources_for_llm(sources)
    })

    return {
        'final_summary': result
    }
