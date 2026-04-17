from abc import ABC, abstractmethod

from src.domain.entities.chat_entity import ChatEntity
from src.domain.results.result import Result


class IAgentClient(ABC):
	@abstractmethod
	async def invoke(self, message: str, athlete_id: int) -> Result[ChatEntity]:
		pass
