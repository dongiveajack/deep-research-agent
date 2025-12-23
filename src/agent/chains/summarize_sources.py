from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from src.agent.prompts.prompts import SUMMARIZE_SOURCES_CHAIN_PROMPT_TEMPLATE_2, \
    SUMMARIZE_SOURCES_CHAIN_PROMPT_TEMPLATE_3

load_dotenv()

# llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)
# llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
# llm = ChatOpenAI(model='gpt-5-mini', temperature=0)
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


class ResearchSummary(BaseModel):
    # description: str = Field(description="1-2 sentence summary of the research for indexing")
    final_summary: str = Field(description="Detailed Report of the research topic")


def summarize_sources_chain():
    system_prompt = PromptTemplate.from_template(template=SUMMARIZE_SOURCES_CHAIN_PROMPT_TEMPLATE_3)
    # return system_prompt | llm.with_structured_output(ResearchSummary)
    return system_prompt | llm | StrOutputParser()
