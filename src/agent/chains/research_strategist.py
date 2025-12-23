from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.agent.prompts.prompts import RESEARCH_STRATEGIST_PROMPT


class SearchQueryPlan(BaseModel):
    """The search plan containing the strategy and list of queries."""

    is_complex: bool = Field(
        description="True if the query requires multi-step research (e.g., market analysis, feasibility). False if it is a simple fact or how-to."
    )
    analysis: str = Field(
        description="Brief reasoning for why this is simple or complex."
    )
    search_queries: List[str] = Field(
        description="The list of 1 to 5 optimized search queries to execute."
    )


# llm = ChatOllama(model='deepseek-r1:8b', reasoning=True, temperature=0)
# llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

def research_strategist_chain():
    system_prompt = PromptTemplate.from_template(RESEARCH_STRATEGIST_PROMPT)
    query_chain = system_prompt | llm.with_structured_output(SearchQueryPlan)
    return query_chain

# if __name__ == '__main__':
#     chain = research_strategist_chain()
#     # chain_input = {
#     #     'user_query': 'I want you to go through spiritual tech space and give me a full report of companies working for this, check SriMandir from apps for bharat and explain if its worth exploring this space to build a 100 million dollar company. consider yourself as an expert researcher and someone who gives me advice on building and adding value by tech in a specific space or sector. ',
#     # }
#     chain_input = {
#         'user_query': 'what is the process behind photosynthesis?'
#     }
#     result = chain.invoke(chain_input)
#     print(result)
