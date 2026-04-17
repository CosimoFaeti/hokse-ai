import httpx

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton
from src.persistence.repositories.strava_token_repository import StravaTokenRepository


class StravaClient(metaclass=Singleton):
	"""Utility class to manage connection with Strava API."""

	def __init__(self, strava_token_repository: StravaTokenRepository):
		self.strava_token_repository = strava_token_repository

	# Public

	@exception_handler
	async def exchange_code(self, code: str) -> Result[StravaTokenEntity]:
		""""""
		logger.info(msg="Start")

		async with httpx.AsyncClient() as client:
			response = await client.post(
				url=SETTINGS.STRAVA_TOKEN_URL,
				data={
					"client_id": SETTINGS.STRAVA_CLIENT_ID,
					"client_secret": SETTINGS.STRAVA_CLIENT_SECRET,
					"code": code,
					"grant_type": "authorization_code",
				},
			)
			response.raise_for_status()
			data = response.json()

		token = StravaTokenEntity(
			athlete_id=data["athlete"]["id"],
			access_token=data["access_token"],
			refresh_token=data["refresh_token"],
			expires_at=data["expires_at"],
			scope=data.get("scope", SETTINGS.STRAVA_SCOPE),
		)

		logger.info(msg="End")
		logger.debug(msg=f"Code exchanged for athlete_id={token.athlete_id}")

		return Result.ok(value=token)

	@exception_handler
	async def refresh_token(self, token: StravaTokenEntity) -> Result[StravaTokenEntity]:
		""""""
		logger.info(msg="Start")
		logger.debug(msg=f"Refreshing Strava token for athlete_id={token.athlete_id}")

		async with httpx.AsyncClient() as client:
			response = await client.post(
				url=SETTINGS.STRAVA_TOKEN_URL,
				data={
					"client_id": SETTINGS.STRAVA_CLIENT_ID,
					"client_secret": SETTINGS.STRAVA_CLIENT_SECRET,
					"grant_type": "refresh_token",
					"refresh_token": token.refresh_token,
				},
			)
			response.raise_for_status()
			data = response.json()

		new_strava_token = StravaTokenEntity(
			athlete_id=token.athlete_id,
			access_token=data["access_token"],
			refresh_token=data["refresh_token"],
			expires_at=data["expires_at"],
			scope=token.scope,
		)

		logger.info(msg="End")

		return Result.ok(value=new_strava_token)

	@exception_handler
	async def get_activities(self, athlete_id: int, per_page: int = 100, page: int = 1) -> Result[list[ActivityEntity]]:
		""""""
		logger.info(msg="Start")

		result_strava_token = await self.strava_token_repository.get(athlete_id=athlete_id)

		if result_strava_token.failed:
			logger.error(msg="An error occurred while retrieving Strava token.")
			return Result.fail(error=result_strava_token.error)

		strava_token = result_strava_token.value

		async with httpx.AsyncClient() as client:
			response = await client.get(
				url=f"{SETTINGS.STRAVA_API_URL}/athlete/activities",
				headers={"Authorization": f"Bearer {strava_token.access_token}"},
				params={"per_page": per_page, "page": page},
			)
			response.raise_for_status()
			data = response.json()

		activities: list[ActivityEntity] = []

		for activity in data:
			activities.append(
				ActivityEntity(
					athlete_id=athlete_id,
					name=activity["name"],
					sport_type=activity["sport_type"],
					distance=activity["distance"],
					moving_time=activity["moving_time"],
					elapsed_time=activity["elapsed_time"],
					total_elevation_gain=activity["total_elevation_gain"],
					elev_high=activity.get("elev_high"),
					elev_low=activity.get("elev_low"),
					average_heartrate=activity.get("average_heartrate"),
					start_date=activity["start_date"],
				)
			)

		logger.info(msg="End")
		logger.debug(msg=f"Return value=list of {len(activities)} activities.")

		return Result.ok(value=activities)
