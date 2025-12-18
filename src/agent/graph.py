"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

import pprint

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.agent.nodes.evaluate_content import analyze_content_node
from src.agent.nodes.generate_query import generate_query_node, research_strategy_node
from src.agent.nodes.review_research_node import review_research_node
from src.agent.nodes.summarize_sources import summarization_sources
from src.agent.nodes.web_search import search_web_node
from src.agent.states.agent_state import AgentState


def web_search_needed(state: AgentState):
    if state['evaluation_result']:
        return "summarization_sources"
    else:
        return "search_web_node"


def start_research(state: AgentState):
    if state['start_research']:
        return "search_web_node"
    else:
        return END


# Define the graph
graph = (
    StateGraph(AgentState)
    .add_node(research_strategy_node)
    .add_node(review_research_node)
    .add_node(search_web_node)
    .add_node(analyze_content_node)
    .add_node(summarization_sources)
    .add_edge(START, "research_strategy_node")
    .add_edge("research_strategy_node", "review_research_node")
    .add_conditional_edges(
        "review_research_node",
        start_research,
        {
            "search_web_node": "search_web_node",
            END: END
        }
    )
    # .add_edge("research_strategy_node", "search_web_node")
    .add_edge("search_web_node", 'analyze_content_node')
    .add_conditional_edges(
        "analyze_content_node",
        web_search_needed,
        {
            "summarization_sources": "summarization_sources",
            "search_web_node": "search_web_node"
        }
    )
    .add_edge("summarization_sources", END)
    .compile(name="ResearchAgent")
)

# graph.get_graph().draw_mermaid_png(output_file_path="graph_image.png")
#
# result = graph.invoke({'topic': 'how to build agents using langgraph'})
# pprint.pprint(result)
#
# pprint.pprint(result['final_summary'])
