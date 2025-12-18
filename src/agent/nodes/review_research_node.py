from langgraph.types import interrupt

from src.agent.states.agent_state import AgentState


def review_research_node(state: AgentState):
    question = {
        'question': 'Review research - Edit/Approve/Reject',
        'user_query': state.get('topic'),
        'Research Websites': state.get('generated_queries')
    }
    user_response = interrupt(question)
    if user_response['start_research'] == 'approved':
        return {
            'start_research': True,
            'generated_queries': user_response['generated_queries']
        }
    else:
        return {
            'start_research': False
        }
