from abc import ABC, abstractmethod

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result


class IStravaTokenRepository(ABC):
	# region GET
	@staticmethod
	@abstractmethod
	async def get(athlete_id: int | None) -> Result[StravaTokenEntity]:
		pass

	# endregion

	# region POST
	@staticmethod
	@abstractmethod
	async def post(token: StravaTokenEntity) -> Result[StravaTokenEntity]:
		pass

	# endregion

	# region DELETE
	@staticmethod
	@abstractmethod
	async def delete(athlete_id: int) -> Result[StravaTokenEntity]:
		pass

	# endregion
