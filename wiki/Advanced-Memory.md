# Advanced Memory System

The Deep Research Agent uses a **Hybrid Memory Architecture** to provide both fast local context and cross-session persistence.

## 🏢 1. Platform Store (Long-Term)
This is the "Corporate Memory" of the agent. It survives even if you delete your local database or start a new thread.

- **Storage**: JSON-based key-value pairs in the LangGraph Server Store.
- **Indexing**: Configured in `langgraph.json` to use OpenAI's `text-embedding-3-small`.
- **Fields Indexed**: `summary`, `first_name`, `last_name`.
- **Use Case**: Checking if we have already researched a topic for a user in a previous session.

### Configuration snippet:
```json
"store": {
  "index": {
    "embed": "openai:text-embedding-3-small", 
    "fields": ["summary"]
  }
}
```

## 💻 2. Local Chroma DB (Short-Term/RAG)
Used for high-speed retrieval of *specific snippets* within a research loop.

- **Technology**: Chroma DB (running locally).
- **Embeddings**: Ollama (`nomic-embed-text`).
- **Use Case**: When the summarizer needs to find the exact quote or statistic among hundreds of search results.

## 🔗 The Sync Process
When a research report is finalized in `save_context_node`:
1.  The final summary is **chunked** and saved to the **Local Chroma DB**.
2.  A high-level metadata entry is **put** into the **Platform Store**.

This ensures that the agent is both "smart locally" (low latency) and "knowledgeable globally" (persistent across devices/sessions).
