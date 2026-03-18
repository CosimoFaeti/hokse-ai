import jsonpatch

from pydantic import UUID4
from beanie.exceptions import DocumentNotFound

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.entities.patch_entity import PatchEntity
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
	async def get(id: UUID4) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		result = await StravaToken.get(docuemnt_id=id)

		if result is None:
			logger.error(msg=f"Entry of type strava token with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

		logger.info(msg="End")

		strava_token: StravaTokenEntity = StravaTokenEntity(**result.model_dump())

		return Result.ok(value=strava_token)
	# endregion

	# region POST
	@exception_handler
	@staticmethod
	async def post(entity: StravaTokenEntity) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		nosql_strava_token: StravaToken = StravaToken(**entity.model_dump())

		await nosql_strava_token.insert()

		logger.info(msg="End")

		return Result.ok(value=entity)
	# endregion

	# region DELETE
	@exception_handler
	@staticmethod
	async def delete(id: UUID4) -> Result[StravaTokenEntity]:
		""""""

		logger.info(msg="Start")

		result = await StravaToken.get(docuemnt_id=id)

		if result is None:
			logger.error(msg=f"Entry of type strava token with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

		await result.delete()

		strava_token: StravaTokenEntity = StravaTokenEntity(**result.model_dump())

		logger.info(msg="End")

		return Result.ok(value=strava_token)
	# endregion