from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from src.agent.prompts.prompts import EVALUATE_CONTENT_CHAIN_PROMPT_TEMPLATE

load_dotenv()

llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)


class ContentEvaluation(BaseModel):
    is_sufficient: bool = Field(description="Whether the content is sufficient to write a detailed report")
    next_search_queries: str = Field(description="The next search queries to gather information from the web")

def evaluate_content_chain():
    system_prompt = PromptTemplate.from_template(template=EVALUATE_CONTENT_CHAIN_PROMPT_TEMPLATE)
    evaluation_chain = system_prompt | llm.with_structured_output(ContentEvaluation)
    return evaluation_chain
