"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.agent.nodes.retrieve_memory_node import retrieve_memory_node
from src.agent.nodes.review_research_node import review_research_node
from src.agent.nodes.router_node import router_node
from src.agent.nodes.evaluate_content import analyze_content_node
from src.agent.nodes.generate_query import research_strategy_node
from src.agent.nodes.save_context_node import save_context_node, save_long_term_memory, get_long_term_memory
from src.agent.nodes.summarize_sources import summarization_sources
from src.agent.nodes.web_search import search_web_node
from src.agent.nodes.assistant_node import assistant_node
from src.agent.states.agent_state import AgentState, TempState


def should_search_web(state: AgentState):
    if state['evaluation_result']:
        return "summarization_sources"
    else:
        return "search_web_node"


def should_search_memory(state: AgentState):
    return state["use_memory"]


def review_research(state: AgentState):
    return state['start_research']


def assistant_router(state: AgentState):
    return state["next_node"]


# Define the graph
graph = (
    StateGraph(AgentState)
    .add_node(assistant_node)
    .add_node(router_node)
    .add_node(retrieve_memory_node)
    .add_node(review_research_node)
    .add_node(research_strategy_node)
    .add_node(search_web_node)
    .add_node(analyze_content_node)
    .add_node(summarization_sources)
    .add_node(save_context_node)
    .add_edge(START, "assistant_node")
    .add_conditional_edges(
        "assistant_node",
        assistant_router,
        {
            "conversation": END,
            "research": "router_node"
        }
    )
    .add_conditional_edges(
        "router_node",
        should_search_memory,
        {
            True: "retrieve_memory_node",
            False: "research_strategy_node"
        }
    )
    .add_edge("retrieve_memory_node", "research_strategy_node")
    .add_edge("research_strategy_node", "review_research_node")
    .add_conditional_edges(
        "review_research_node",
        review_research,
        {
            True: "search_web_node",
            False: END
        }
    )
    .add_edge("search_web_node", 'analyze_content_node')
    .add_conditional_edges(
        "analyze_content_node",
        should_search_web,
        {
            "summarization_sources": "summarization_sources",
            "search_web_node": "search_web_node"
        }
    )
    .add_edge("summarization_sources", "save_context_node")
    .add_edge("save_context_node", END)
    .compile(name="ResearchAgent")
)

# graph = (
#     StateGraph(TempState)
#     .add_node(save_long_term_memory)
#     .add_node(get_long_term_memory)
#     .add_edge(START, "save_long_term_memory")
#     .add_edge("save_long_term_memory", "get_long_term_memory")
#     .add_edge("get_long_term_memory", END)
#     .compile(name="ResearchAgent")
# )
