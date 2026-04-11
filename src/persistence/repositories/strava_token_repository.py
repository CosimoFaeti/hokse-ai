from datetime import timezone

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.objects.nosql_strava_token import StravaToken


class StravaTokenRepository:
	"""Repository to perform operations on strava token NoSQL collection."""

	# region GET
	@exception_handler
	@staticmethod
	async def get(athlete_id: int | None) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		result = await StravaToken.find_one(StravaToken.athlete_id == athlete_id)

		if result is None:
			logger.error(msg=f"Entry of type strava token with key={athlete_id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=str(athlete_id)))

		logger.info(msg="End")

		strava_token: StravaTokenEntity = StravaTokenEntity(
			athlete_id=result.athlete_id,
			access_token=result.access_token,
			refresh_token=result.refresh_token,
			expires_at=result.expires_at.replace(tzinfo=timezone.utc),
			scope=result.scope,
		)

		return Result.ok(value=strava_token)
	# endregion

	# region POST
	@exception_handler
	@staticmethod
	async def post(token: StravaTokenEntity) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		nosql_strava_token: StravaToken = StravaToken(**token.model_dump())

		await nosql_strava_token.insert()

		logger.info(msg="End")

		return Result.ok(value=token)
	# endregion

	# region DELETE
	@exception_handler
	@staticmethod
	async def delete(athlete_id: int | None) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		result = await StravaToken.find_one(StravaToken.athlete_id == athlete_id)

		if result is None:
			logger.error(msg=f"Entry of type strava token with key={athlete_id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=str(athlete_id)))

		await result.delete()

		strava_token: StravaTokenEntity = StravaTokenEntity(**result.model_dump())

		logger.info(msg="End")

		return Result.ok(value=strava_token)
	# endregion