from src.agent.states.agent_state import AgentState
from src.agent.utils.search import duckduckgo_web_search, tavily_search


def search_web_node(state: AgentState):
   queries = state['generated_queries']
   results = tavily_search(queries)
   return {
       'source_documents': results
   }


# if __name__ == '__main__':
#     state = {
#         'topic': 'langgraph',
#         'generated_queries': ['how to build langchain agents'],
#         'source_documents': [],
#         'final_summary': ''
#     }
#     result = search_web_node(state)