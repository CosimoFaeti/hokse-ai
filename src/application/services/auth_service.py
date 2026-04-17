from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.domain.utilities.exception_handler import exception_handler
from src.application.clients.i_strava_client import IStravaClient
from src.application.interfaces.i_auth_service import IAuthService
from src.application.repositories.i_strava_token_repository import IStravaTokenRepository


class AuthService(IAuthService):
	"""Forwards requests to Strava token repository and Strava client."""

	def __init__(self, strava_token_repository: IStravaTokenRepository, strava_client: IStravaClient):
		self.strava_token_repository = strava_token_repository
		self.strava_client = strava_client

	# region POST
	@exception_handler
	async def exchange_code(self, code: str) -> Result[StravaTokenEntity]:
		""""""
		logger.info(msg="Start")

		result_exchange_code: Result[StravaTokenEntity] = await self.strava_client.exchange_code(code=code)

		if result_exchange_code.failed:
			logger.error(msg="An error occurred while exchange code.")
			return Result.fail(error=result_exchange_code.error)

		token: StravaTokenEntity = result_exchange_code.value

		await self.strava_token_repository.post(token=token)

		logger.debug(msg=f"Token exchanged and upserted for athlete_id={token.athlete_id}")
		logger.info(msg="End")

		return Result.ok(value=token)

	# endregion

	# region GET
	@exception_handler
	async def get_valid_token(self, athlete_id: int) -> Result[StravaTokenEntity]:
		""""""
		logger.info(msg="Start")
		logger.debug(msg=f"Getting valid token for athlete_id={athlete_id}")

		result_get_token: Result[StravaTokenEntity] = await self.strava_token_repository.get(athlete_id=athlete_id)

		if result_get_token.failed:
			logger.error(msg="An error occurred while getting valid token.")
			return Result.fail(error=result_get_token.error)

		token: StravaTokenEntity = result_get_token.value

		if token.refresh():
			logger.debug(msg="Refreshing token.")
			result_refresh_token: Result[StravaTokenEntity] = await self._refresh_token(token)
			token: StravaTokenEntity = result_refresh_token.value

		logger.info(msg="End")

		return Result.ok(value=token)

	# endregion

	# region DELETE
	@exception_handler
	async def revoke(self, athlete_id: int) -> Result[StravaTokenEntity]:
		""""""
		logger.info(msg="Start")
		logger.debug(msg=f"Revoking token for athlete_id={athlete_id}")

		result_revoke: Result[StravaTokenEntity] = await self.strava_token_repository.delete(athlete_id=athlete_id)

		if result_revoke.failed:
			logger.error(msg="An error occurred while revoking token.")
			return Result.fail(error=result_revoke.error)

		token: StravaTokenEntity = result_revoke.value

		logger.info(msg="End")

		return Result.ok(value=token)

	# endregion

	# Private
	@exception_handler
	async def _refresh_token(self, token: StravaTokenEntity) -> Result[StravaTokenEntity]:
		""""""
		logger.debug(msg=f"Refreshing token for athlete_id={token.athlete_id}")

		result_refresh_token: Result[StravaTokenEntity] = await self.strava_client.refresh_token(token=token)

		if result_refresh_token.failed:
			logger.error(msg="An error occurred while refreshing token.")
			return Result.fail(error=result_refresh_token.error)

		refreshed_token: StravaTokenEntity = result_refresh_token.value

		await self.strava_token_repository.post(token=refreshed_token)

		logger.info(msg="End")
		return Result.ok(value=refreshed_token)
