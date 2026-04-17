from typing import Literal
from langgraph.graph import END

from src.domain.entities.agent_state_entity import AgentState


def should_continue(state: AgentState) -> Literal["tool_node", END]:
	""""""
	messages = state.messages
	last_message = messages[-1]

	if last_message.tool_calls:
		return "tool_node"

	return END
