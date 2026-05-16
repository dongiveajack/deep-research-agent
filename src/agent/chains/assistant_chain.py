from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from src.agent.prompts.prompts import ASSISTANT_PROMPT


class AssistantDecision(BaseModel):
    """The decision and potential response from the assistant."""
    reasoning: str = Field(description="Brief explanation of the decision.")
    is_research: bool = Field(description="True if deep research is needed.")
    topic: str = Field(description="The research topic extracted (if is_research is True).")
    response: str = Field(description="Direct response to the user (if is_research is False).")


llm = ChatOpenAI(model='gpt-5-nano', temperature=0)

def assistant_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", ASSISTANT_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ])
    chain = prompt | llm.with_structured_output(AssistantDecision)
    return chain
