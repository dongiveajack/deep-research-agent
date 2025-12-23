import pprint
from src.agent.graph import graph

def run_test():
    # TEST 1: Initial Research (Build Memory)
    topic_1 = "What is the history of LangGraph and its core features?"
    print(f"\n--- RUNNING TEST 1: {topic_1} ---")
    
    initial_state_1 = {
        "topic": topic_1,
        "generated_queries": [],
        "past_queries": [],
        "source_documents": [],
        "final_summary": "",
        "evaluation_result": False,
        "memory_context": "",
        "use_memory": False
    }
    
    result_1 = graph.invoke(initial_state_1)
    print("\nTest 1 Summary Header:")
    print(result_1["final_summary"][:500] + "...")
    
    # Check if memory was saved (manual check of files after run)
    
    # TEST 2: Related Research (Trigger Memory)
    topic_2 = "Compare LangGraph with other agentic frameworks like AutoGen and CrewAI."
    print(f"\n--- RUNNING TEST 2: {topic_2} ---")
    
    initial_state_2 = {
        "topic": topic_2,
        "generated_queries": [],
        "past_queries": [],
        "source_documents": [],
        "final_summary": "",
        "evaluation_result": False,
        "memory_context": "",
        "use_memory": False
    }
    
    result_2 = graph.invoke(initial_state_2)
    
    print("\nTest 2 Router Decision:")
    print(f"Use Memory: {result_2.get('use_memory')}")
    
    print("\nTest 2 Summary Header:")
    print(result_2["final_summary"][:500] + "...")

if __name__ == "__main__":
    run_test()
