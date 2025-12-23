from langgraph.types import Overwrite

from src.agent.chains.evaluate_content_chain import evaluate_content_chain, ContentEvaluation
from src.agent.states.agent_state import AgentState
from src.agent.utils.common import format_sources_for_llm


def analyze_content_node(state: AgentState):
    input = {
        'topic': state['topic'],
        'web_content': format_sources_for_llm(state['source_documents']),
    }
    result: ContentEvaluation = evaluate_content_chain().invoke(input)
    return {
        'evaluation_result': result.is_sufficient,
        'past_queries': state['generated_queries'],
        'generated_queries': state['generated_queries'] if result.is_sufficient else result.next_search_queries
    }
