from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from src.agent.prompts.prompts import GENERATE_QUERY_CHAIN_PROMPT_TEMPLATE, GENERATE_QUERY_CHAIN_PROMPT_TEMPLATE_1

load_dotenv()

llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)


class GeneratedQueries(BaseModel):
    queries: list[str]


def generate_query_chain():
    system_prompt = PromptTemplate.from_template(template=GENERATE_QUERY_CHAIN_PROMPT_TEMPLATE)
    query_chain = system_prompt | llm.with_structured_output(GeneratedQueries)
    return query_chain


# if __name__ == '__main__':
#     chain = generate_query_chain()
#     chain_input = {
#         'topic': 'how to build a langgraph agent',
#         'past_queries': ''
#     }
#     result = chain.invoke(chain_input)
#     print(result.queries)
