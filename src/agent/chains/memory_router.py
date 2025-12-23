from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from src.agent.prompts.prompts import MEMORY_ROUTER_PROMPT

class MemoryRoute(BaseModel):
    """The routing decision for long-term memory."""
    reasoning: str = Field(description="Brief explanation of why memory search is or isn't needed.")
    use_memory: bool = Field(description="True if the query likely has relevant history in the database.")

llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)

def memory_router_chain():
    system_prompt = PromptTemplate.from_template(MEMORY_ROUTER_PROMPT)
    router_chain = system_prompt | llm.with_structured_output(MemoryRoute)
    return router_chain
