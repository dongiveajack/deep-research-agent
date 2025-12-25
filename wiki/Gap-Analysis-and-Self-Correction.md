# Gap Analysis and Self-Correction

The "Deep" in Deep Research Agent comes from the agent's ability to self-correct. It doesn't just perform a keyword search and summarize; it evaluates its own understanding and identifies what it *doesn't* know.

## 🧠 The Brain: Analyze Content Node
The `analyze_content_node` is the gatekeeper of the research loop. It uses the `Evaluate Content Chain` to perform a rigorous assessment of the gathered information.

### How it works:
1.  **Context Assembly**: All retrieved snippets from the web search are formatted into a single context block.
2.  **Pydantic Evaluation**: The LLM is forced to output a `ContentEvaluation` object:
    - `is_sufficient`: A boolean check on whether the goal is met.
    - `reasoning`: The "why" behind the decision.
    - `next_search_queries`: A list of targeted queries to find the missing pieces.

## 🔍 The Evaluation Criteria
The agent is instructed (via prompts) to look for:
- **Depth**: Are the definitions clear and technical?
- **Actionability**: Could a user make a decision based on this info (e.g., "Is it worth building a $100M company in this space?")?
- **Recency**: If the topic is dynamic (like AI or spiritual tech), is the data from current years?
- **Contradictions**: Does Source A say X and Source B say Y? If so, the agent flags a "Gap" to investigate the discrepancy.

## 🔄 The Recursive Loop
If `is_sufficient` is `False`:
- The `evaluation_result` in the state is set to `False`.
- The graph transitions back to `search_web_node`.
- **Crucially**, it uses the `next_search_queries` generated *during* the evaluation, rather than reusing the initial strategy. This ensures each loop gets more specific and fills the exact knowledge gaps identified.

## 🛠️ Implementation Snippet
```python
# From evaluate_content.py
return {
    'evaluation_result': result.is_sufficient,
    'past_queries': state['generated_queries'], # Keeps history for visibility
    'generated_queries': state['generated_queries'] if result.is_sufficient else result.next_search_queries
}
```
This logic ensures that if we stop early, we at least have the strategy, but if we continue, we have a new, sharper plan.
