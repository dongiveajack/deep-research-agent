from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from src.agent.prompts.prompts import SUMMARIZE_SOURCES_CHAIN_PROMPT_TEMPLATE_2

load_dotenv()

llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)


def summarize_sources_chain():
    system_prompt = PromptTemplate.from_template(template=SUMMARIZE_SOURCES_CHAIN_PROMPT_TEMPLATE_2)

    return system_prompt | llm | StrOutputParser()
