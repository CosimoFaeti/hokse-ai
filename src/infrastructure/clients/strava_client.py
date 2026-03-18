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

    def __init__(self, strava_token_repo: StravaTokenRepository):
        self._strava_token_repo = strava_token_repo

    # Public

    @exception_handler
    async def get_activities(self, athlete_id: int, per_page: int = 100, page: int = 1) -> Result[list[ActivityEntity]]:
        """"""
        logger.info(msg="Start")

        result_strava_token = await self._get_valid_token(athlete_id)
        strava_token = result_strava_token.value

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{SETTINGS.STRAVA_API_URL}/athlete/activities",
                headers={"Authorization": f"Bearer {strava_token.access_token}"},
                params={"per_page": per_page, "page": page},
            )
            response.raise_for_status()
            data = response.json()

        result: list[ActivityEntity] = []

        for activity in data:
            result.append(ActivityEntity(
                athlete_id=athlete_id,
                name=activity.name,
                sport_type=activity.sport_type,
                distance=activity.distance,
                moving_time=activity.moving_time,
                elapsed_time=activity.elapsed_time,
                total_elevation_gain=activity.total_elevation_gain,
                elev_high=activity.elev_high,
                elev_low=activity.elev_low,
                start_date=activity.start_date,
            ))

        logger.info(msg="End")
        logger.debug(msg=f"Return value=list of {len(result)} activities.")

        return Result.ok(value=result)

    # Private

    @exception_handler
    async def _get_valid_token(self, athlete_id: int | None = None) -> Result[StravaTokenEntity]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Getting valid Strava token with key={athlete_id}")

        result_strava_token = await self._strava_token_repo.get(athlete_id)
        strava_token = result_strava_token.value

        # TODO: if strava_token is None?

        if strava_token.refresh():
            result_strava_token = self._refresh_token(strava_token)
            strava_token = result_strava_token.value

        logger.info(msg="End")

        return Result.ok(value=strava_token)

    @exception_handler
    async def _refresh_token(self, strava_token: StravaTokenEntity) -> Result[StravaTokenEntity]:
        """"""
        logger.info(msg="Start")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=SETTINGS.STRAVA_TOKEN_URL,
                data={
                    "client_id": SETTINGS.STRAVA_CLIENT_ID,
                    "client_secret": SETTINGS.STRAVA_CLIENT_SECRET,
                    "grant_type": "refresh_token",
                    "refresh_token": strava_token.refresh_token,
                }
            )
            response.raise_for_status()
            data = response.json()

        new_strava_token = StravaTokenEntity(
            athlete_id=strava_token.athlete_id,
            access_token=data.access_token,
            refresh_token=data.refresh_token,
            expires_at=data.expires_at,
            scope=strava_token.scope,
        )

        await self._strava_token_repo.post(new_strava_token)

        logger.info(msg="End")

        return Result.ok(value=new_strava_token)











