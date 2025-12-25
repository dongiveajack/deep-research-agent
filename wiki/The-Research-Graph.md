# The Research Graph

The core of the Deep Research Agent is a **LangGraph StateGraph**. This allows for complex, cyclical workflows that a standard linear chain cannot handle.

## 🔄 The Life of a Research Request

1.  **Entry Point**: The request begins at the `router_node`.
2.  **Memory Recall**: Before hitting the web, the agent checks the **Platform Store** to see if a similar topic has been researched recently.
3.  **Strategy Generation**: The `research_strategy_node` uses a Pydantic model (`SearchQueryPlan`) to break the topic into 1-5 sub-queries.
4.  **The Pause**: The graph reaches the `review_research_node` and **interrupts**. This is where the user approves the queries.
5.  **Investigation**: Once approved, the `search_web_node` executes queries via Tavily and DuckDuckGo.
6.  **Quality Check**: The `analyze_content_node` performs a "Gap Analysis." If the content isn't deep enough, it updates the state with new queries and **loops back** to step 5.
7.  **Final Synthesis**: Once satisfied, the `summarization_sources` node writes the final report.

## 💾 State Reducers
One of our most powerful features is the use of **Reducers** in the `AgentState`. This allows us to keep a running history of our research without losing data during loops:

```python
class AgentState(TypedDict):
    # 'operator.add' ensures new queries are appended, not overwritten
    past_queries: Annotated[list[str], operator.add]
    
    # Allows us to accumulate snippets from multiple search loops
    source_documents: Annotated[list[dict[str, str]], operator.add]
```

## 🛠️ Performance
We use **LLM Structured Output** at every decision-making node to ensure the graph never "wanders" or fails to parse a response. Each transition is governed by strict Pydantic models.
