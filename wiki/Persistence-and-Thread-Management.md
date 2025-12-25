# Persistence and Thread Management

Managing state in an autonomous agent is complex. This project distinguishes between **Short-term Conversation State** and **Long-term Global Memory**.

## 🧵 Thread Persistence (Short-term)
Every research session has a unique `thread_id`. The "state" of the graph (which research papers are currently loaded, what loops we've done) is saved to the **Checkpointer**.

- **Implementation**: The graph is compiled with a `PostgresCheckpointer` (in production) or a local pickled checkpointer during development.
- **Why it matters**: If you close your browser or the server crashes mid-research, you can resume exactly where the agent paused (e.g., at the Human-in-the-loop interrupt).
- **Reducers**: We use `operator.add` in the state to ensure that as the agent loops, it *accumulates* knowledge rather than overwriting it.

## 🏢 Platform Store (Long-term)
Unlike thread state, the **Store** is shared across all threads and users.

- **Storage**: JSON-based key-value pairs.
- **Persistence**: Managed by the LangGraph Server runtime.
- **The Router Node**: When a new request comes in, the `router_node` checks this store first. If the research has already been done for a similar topic, it can suggest using the existing memory instead of starting a new expensive web search.

## 🔄 The Difference: Checkpointer vs Store

| Feature | Checkpointer (State) | Store (Memory) |
| :--- | :--- | :--- |
| **Scope** | Single Thread / Session | Global / Across Sessions |
| **Data Type** | The entire `AgentState` | Curated JSON (e.g., Summaries) |
| **Search** | Exact Thread ID only | **Semantic Search** (Vector-indexed) |
| **Lifecycle** | Often transient/ephemeral | Persistent / Long-term |

## 🚀 Semantic Search Integration
We explicitly configure the store in `langgraph.json` to enable vector search. This allows the `router_node` to find "conceptually similar" research even if the user phrasing is slightly different.

```json
"store": {
  "index": {
    "embed": "openai:text-embedding-3-small", 
    "fields": ["summary"] 
  }
}
```
*Note: Fields listed in `fields` are the ONLY ones that can be searched via the `store.search()` method.*
