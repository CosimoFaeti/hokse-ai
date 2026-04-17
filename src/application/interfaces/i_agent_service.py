from abc import ABC, abstractmethod

from src.domain.entities.chat_entity import ChatEntity
from src.domain.results.result import Result


class IAgentService(ABC):
	@staticmethod
	@abstractmethod
	async def run(message: str, athlete_id: int) -> Result[ChatEntity]:
		pass
