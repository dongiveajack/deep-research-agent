from typing import Any

from src.agent.states.agent_state import AgentState
from src.agent.chains.research_strategist import research_strategist_chain, SearchQueryPlan


def research_strategy_node(state: AgentState) -> dict[str, Any]:
    chain_input = {
        'user_query': state['topic'],
        'context': state.get('memory_context', '')
    }
    query_plan: SearchQueryPlan = research_strategist_chain().invoke(chain_input)
    return {
        'generated_queries': query_plan.search_queries
    }
