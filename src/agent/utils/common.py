from typing import List, Dict, Any


def format_sources_for_llm(source_documents: List[Dict[str, Any]]) -> str:
    formatted_sources = []

    for i, doc in enumerate(source_documents, 1):
        # 1. Start a new source block with a clear separator and header
        context_block = f"""
                --- SOURCE DOCUMENT {i} ---
                TITLE: {doc.get('title', 'N/A')}
                URL: {doc.get('url', 'N/A')}
                SEARCH QUERY USED: {doc.get('search_query', 'N/A')}

                ### SNIPPET CONTENT:
                {doc.get('snippet', 'No content snippet available.')}
            """
        formatted_sources.append(context_block)

    # 2. Join all the individual source blocks into one final string
    return "\n".join(formatted_sources)
