import os
import json
from typing import List, Dict, Optional
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Path to the research index
INDEX_PATH = os.path.join(os.getcwd(), "research_index.json")
CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")

def get_embeddings():
    # Use default local Ollama URL (11434) if not otherwise specified or proxied
    return OllamaEmbeddings(model="nomic-embed-text:latest")

def get_vector_store():
    # Ensure directory exists
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH, exist_ok=True)
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings(),
        collection_name="research_memory"
    )

def save_summary(topic: str, summary: str, description: str):
    """Save summary to vector store and update the topic index."""
    print(f"DEBUG: Saving summary for topic: {topic}")
    print(f"DEBUG: Summary length: {len(summary)} characters")
    
    # 1. Save to Vector Store
    vector_store = get_vector_store()
    
    # Chunk the summary to avoid Ollama embedding limits/crashes
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    chunks = text_splitter.split_text(summary)
    print(f"DEBUG: Split summary into {len(chunks)} chunks")
    
    docs = [
        Document(
            page_content=chunk,
            metadata={"topic": topic, "description": description, "chunk": i}
        )
        for i, chunk in enumerate(chunks)
    ]
    
    try:
        vector_store.add_documents(docs)
        print("DEBUG: Successfully added documents to vector store")
    except Exception as e:
        print(f"ERROR: Failed to add documents to vector store: {e}")
        # Re-raise to let the graph know it failed
        raise
    
    # 2. Update JSON Index
    index = []
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r") as f:
                index = json.load(f)
        except Exception:
            index = []
            
    # Add new entry
    index.append({
        "topic": topic,
        "description": description
    })
    
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

    return {}

def retrieve_context(query: str, k: int = 1) -> str:
    """Retrieve relevant past research context."""
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    
    if not results:
        return ""
    
    context_parts = []
    for doc in results:
        part = f"### Past Research: {doc.metadata.get('topic')}\n{doc.page_content}"
        context_parts.append(part)
        
    return "\n\n".join(context_parts)

def get_research_index() -> List[Dict[str, str]]:
    """Get the list of previously researched topics."""
    if not os.path.exists(INDEX_PATH):
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        return []
    try:
        with open(INDEX_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []
