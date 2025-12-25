# Human-in-the-loop (HIL)

Research can be expensive (API credits) and sensitive. We use the **Interrupt Pattern** to ensure a human is always in the driver's seat.

## ⏸️ The Interrupt Node
In `src/agent/nodes/review_research_node.py`, the agent calls:
```python
user_response = interrupt(question)
```

This causes the LangGraph engine to **halt execution**. The state is persisted, and the agent waits for an external signal from the API or the UI.

## 🚦 Approval States
When the agent is paused, the user is presented with the **Research Plan**:
- **Topic**: What are we looking for?
- **Analysis**: Why does the AI think this is complex/simple?
- **Proposed Queries**: The specific terms the AI wants to use on Google/Tavily.

### User Actions:
1.  **Approve**: The agent proceeds immediately to web search.
2.  **Modify Queries**: The user can manually edit the list of search queries in the UI. The agent will use the **modified** list.
3.  **Reject**: The execution ends safely without making any expensive API calls.

## 🛠️ Implementation Detail
Our node is designed to be resilient. If a user provides an empty list of queries, the node gracefully falls back to the AI-generated ones to ensure the thread doesn't crash:

```python
'generated_queries': user_response.get('generated_queries') or state.get('generated_queries')
```
