from typing import Any

from src.agent.chains.generate_query_chain import generate_query_chain
from src.agent.states.agent_state import AgentState
from src.agent.chains.research_strategist import research_strategist_chain, SearchQueryPlan


def generate_query_node(state: AgentState) -> dict[str, Any]:
    topic = state['topic']

    chain_input = {
        'topic': topic,
        'past_queries': state.get('generated_queries')
    }
    result = generate_query_chain().invoke(chain_input)

    return {
        'generated_queries': result.queries
    }


# if __name__ == '__main__':
#     state = {
#         'topic': 'langgraph',
#         'generated_queries': '',
#         'source_documents': [],
#         'final_summary': ''
#     }
#     result = generate_query_node(state)
#     print(result)

def research_strategy_node(state: AgentState) -> dict[str, Any]:
    chain_input = {
        'user_query': state['topic']
    }
    query_plan: SearchQueryPlan = research_strategist_chain().invoke(chain_input)
    return {
        'generated_queries': query_plan.search_queries
    }