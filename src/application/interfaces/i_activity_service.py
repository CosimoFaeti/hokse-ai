from abc import ABC, abstractmethod

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.results.result import Result


class IActivityService(ABC):
	# region POST
	@staticmethod
	@abstractmethod
	async def sync(athlete_id: int, pages: int) -> Result[list[ActivityEntity]]:
		pass

	# endregion

	# region GET
	@staticmethod
	@abstractmethod
	async def get(
		athlete_id: int, sport_type: str | None, limit: int, start: str, end: str
	) -> Result[list[ActivityEntity]]:
		pass

	# endregion
