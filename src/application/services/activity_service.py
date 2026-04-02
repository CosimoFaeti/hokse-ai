from typing import Type

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.domain.utilities.exception_handler import exception_handler
from src.application.clients.i_strava_client import IStravaClient
from src.application.interfaces.i_activity_service import IActivityService
from src.application.interfaces.i_auth_service import IAuthService
from src.application.repositories.i_activity_repository import IActivityRepository


class ActivityService(IActivityService):
    """"""

    def __init__(self, activity_repository: Type[IActivityRepository], strava_client: Type[IStravaClient], auth_service: IAuthService):
        self.activity_repository = activity_repository
        self.strava_client = strava_client
        self.auth_service = auth_service

    # region POST
    @exception_handler
    async def sync(self, athlete_id: int, pages: int) -> Result[list[ActivityEntity]]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Syncing activities for athlete {athlete_id} - pages {pages}")

        result_token: Result[StravaTokenEntity] = await self.auth_service.get_valid_token(athlete_id=athlete_id)

        if result_token.failed:
            logger.error(msg="An error occurred while getting valid token")
            return Result.fail(error=result_token.error)

        all_activities: list[ActivityEntity] = []

        for page in range(1, pages + 1):
            result_activities: Result[list[ActivityEntity]] = await self.strava_client.get_activities(athlete_id=athlete_id, per_page=100, page=page)

            if result_activities.failed:
                logger.error(msg="An error occurred while getting activities")
                return Result.fail(error=result_activities.error)

            batch = result_activities.value

            all_activities.extend(batch)

        if all_activities:
            result_upsert: Result[list[ActivityEntity]] = await self.activity_repository.post(activities=all_activities)

            if result_upsert.failed:
                logger.error(msg="An error occurred while posting activities")
                return Result.fail(error=result_upsert.error)

        logger.info(msg="End")
        logger.debug(msg=f"Synced {len(all_activities)} activities.")

        return Result.ok(value=all_activities)
    # endregion

    # region GET
    @exception_handler
    async def get(self, athlete_id: int, sport_type: str | None, limit: int, start: str, end: str) -> Result[list[ActivityEntity]]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Getting activities for athlete {athlete_id} - sport type {sport_type} - limit {limit} - start {start} - end {end}")

        result_get: Result[list[ActivityEntity]] = await self.activity_repository.get(athlete_id=athlete_id, sport_type=sport_type, limit=limit, start=start)

        if result_get.failed:
            logger.error(msg="An error occurred while getting activities")
            return Result.fail(error=result_get.error)

        activities: list[ActivityEntity] = result_get.value

        logger.info(msg="End")

        return Result.ok(value=activities)
    # endregion

