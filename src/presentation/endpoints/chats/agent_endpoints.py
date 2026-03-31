from fastapi import APIRouter, Depends, Body, HTTPException

from dependencies import get_agent_service # TODO
from src.application.services.agent_service import AgentService # TODO
from src.presentation.DTOs.agent.post_chats_input_dto import PostChatInputDTO # TODO
from src.presentation.examples.agent.post_chat_response_examples import POST_CHATS_RESPONSE_EXAMPLES # TODO


agent_router = APIRouter(prefix="/agent", tags=["Agent"])

# Region POST
@agent_router.post(
    path="/chat",
    summary="Create a new chat.",
    description="Create a new chat.",
    status_code=201,
    responses=POST_CHATS_RESPONSE_EXAMPLES,
)
async def chat(
        dto: PostChatInputDTO = Body(examples=POST_CHATS_RESPONSE_EXAMPLES),
        agent_service: AgentService = Depends(get_agent_service)
)
# endregion