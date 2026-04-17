from abc import ABC, abstractmethod

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result


class IAuthService(ABC):
	# region POST
	@staticmethod
	@abstractmethod
	async def exchange_code(code: str) -> Result[StravaTokenEntity]:
		pass

	# endregion

	# region GET
	@staticmethod
	@abstractmethod
	async def get_valid_token(athlete_id: int) -> Result[StravaTokenEntity]:
		pass

	# endregion

	# region DELETE
	@staticmethod
	@abstractmethod
	async def revoke(athlete_id: int) -> Result[StravaTokenEntity]:
		pass

	# endregion
