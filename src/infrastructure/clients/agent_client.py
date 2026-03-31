import uuid
import time
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool

from src.domain.entities.chat_entity import ChatEntity
from src.domain.results.result import Result
from src.domain.utilities.singleton import Singleton
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.exception_handler import exception_handler
from src.infrastructure.llm.llm import model
from src.infrastructure.graph.graph import build_graph

class AgentClient(metaclass=Singleton):
    """Utility class to manage connections to AI models."""

    def __init__(self):

        logger.info(msg="Start")

        self.model = model()

        logger.info(msg="End")

    @exception_handler
    async def invoke(self, message: str, athlete_id: int, tools: list[BaseTool]) -> Result[ChatEntity]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Input params: message={message}, athlete_id={athlete_id}")

        generation_start_time: float = time.time()

        graph = build_graph(model=model, tools=tools)

        initial_state = {
            "messages": [HumanMessage(content=message)],
            "athlete_id": athlete_id
        }

        result_state = await graph.ainvoke(initial_state=initial_state)

        generation_time: float = time.time() - generation_start_time

        chat_entity: ChatEntity = ChatEntity(
            id=uuid.uuid4(),
            message=result_state["messages"][-1].content,
            generation_time=generation_time,
        )

        logger.info(msg="End")

        return Result.ok(value=chat_entity)




