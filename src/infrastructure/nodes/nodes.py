from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage

from src.domain.entities.agent_state_entity import AgentState
from src.domain.templates.prompt import system_prompt

def make_model_node(model_with_tools: BaseChatModel):
    """"""

    async def llm_call(state: AgentState) -> dict:
        """LLM decides whether to call a tool or not."""

        messages = [SystemMessage(content=system_prompt), *state.messages]
        response = await model_with_tools.ainvoke(messages)

        return {"messages": [response]}

    return llm_call
