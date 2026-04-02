from src.domain.entities.chat_entity import ChatEntity
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.application.clients.i_agent_client import IAgentClient
from src.application.interfaces.i_activity_service import IActivityService
from src.application.interfaces.i_agent_service import IAgentService


class AgentService(IAgentService):
    """Owns tool assembly and agent invocation."""

    def __init__(self, activity_service: IActivityService, agent_client: IAgentClient):
        self.activity_service = activity_service
        self.agent_client = agent_client

    @exception_handler
    async def run(self, message: str, athlete_id: int) -> Result[ChatEntity]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Running LangGraph agent for athlete {athlete_id}")

        result_generation: Result[ChatEntity] = await self.agent_client.invoke(message=message, athlete_id=athlete_id)

        if result_generation.failed:
            logger.error(msg=f"An error occurred while running LangGraph agent for athlete {athlete_id}")
            return Result.fail(error=result_generation.error)

        chat: ChatEntity = result_generation.value

        logger.info(msg="End")

        return Result.ok(value=chat)
