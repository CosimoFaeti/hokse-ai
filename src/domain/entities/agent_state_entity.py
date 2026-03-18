from typing import Annotated
from pydantic import BaseModel

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(BaseModel):
    """"""
    messages: Annotated[list[BaseMessage], add_messages]
    athlete_id: int