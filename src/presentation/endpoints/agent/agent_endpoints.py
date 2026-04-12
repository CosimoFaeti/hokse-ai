from fastapi import APIRouter, Depends, Body, HTTPException

from src.dependencies import get_agent_service, get_activity_service
from src.domain.entities.chat_entity import ChatEntity
from src.domain.entities.activity_entity import ActivityEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.application.interfaces.i_agent_service import IAgentService
from src.application.interfaces.i_activity_service import IActivityService
from src.presentation.DTOs.agent.chat.post_chat_input_dto import PostChatInputDTO
from src.presentation.DTOs.agent.chat.post_chat_output_dto import PostChatOutputDTO
from src.presentation.DTOs.agent.sync.post_sync_input_dto import PostSyncInputDTO
from src.presentation.DTOs.agent.sync.post_sync_output_dto import PostSyncOutputDTO
from src.presentation.examples.agent.post_chat_response_examples import POST_CHAT_RESPONSE_EXAMPLES
from src.presentation.examples.agent.post_chat_request_examples import POST_CHAT_BODY_EXAMPLES
from src.presentation.examples.agent.post_sync_response_examples import POST_SYNC_RESPONSE_EXAMPLES
from src.presentation.examples.agent.post_sync_request_examples import POST_SYNC_BODY_EXAMPLES
from src.presentation.mappers.agent.post_chat_mappers import PostChatMappers
from src.presentation.mappers.agent.post_sync_mappers import PostSyncMappers

agent_router = APIRouter(prefix="/agent", tags=["Agent"])

# region POST
@agent_router.post(
    path="/chat",
    summary="Create a new chat.",
    description="Create a new chat.",
    status_code=201,
    responses=POST_CHAT_RESPONSE_EXAMPLES,
)
async def chat(
        dto: PostChatInputDTO = Body(examples=POST_CHAT_BODY_EXAMPLES),
        agent_service: IAgentService = Depends(get_agent_service)
) -> PostChatOutputDTO:
    """"""
    logger.info(msg="Calling POST /chat")

    result: Result[ChatEntity] = await agent_service.run(message=dto.message, athlete_id=dto.athlete_id)

    if result.failed:
        raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

    output: PostChatOutputDTO = PostChatMappers.to_dto(entity=result.value)

    logger.info(msg="Successfully returning from POST /chat")

    return output

@agent_router.post(
    path="/sync",
    summary="Create a new sync.",
    description="Create a new sync.",
    status_code=201,
    responses=POST_SYNC_RESPONSE_EXAMPLES,
)
async def sync(
        dto: PostSyncInputDTO = Body(examples=POST_SYNC_BODY_EXAMPLES),
        activity_service: IActivityService = Depends(get_activity_service),
) -> list[PostSyncOutputDTO]:
    """"""
    logger.info(msg="Calling POST /sync")

    result: Result[list[ActivityEntity]] = await activity_service.sync(athlete_id=dto.athlete_id, pages=dto.pages)

    if result.failed:
        raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

    output: list[PostSyncOutputDTO] = [PostSyncMappers.to_dto(entity=entity) for entity in result.value]

    logger.info(msg="Successfully returning from POST /sync")

    return output
# endregion