from typing import Type

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.domain.utilities.exception_handler import exception_handler
from src.application.clients.i_strava_client import IStravaClient # TODO
from src.application.interfaces.i_activity_service import IActivityService
from src.application.interfaces.i_auth_service import IAuthService
from src.application.repositories.i_activity_repository import IActivityRepository # TODO


class ActivityService(IActivityService):
    """"""

    def __init__(self, activity_repository: Type[IActivityRepository], strava_client: Type[IStravaClient], auth_service: IAuthService):
        self.activity_repository = activity_repository
        self.strava_client = strava_client
        self.auth_service = auth_service

    @exception_handler
    async def sync(self, athlete_id: int, pages: int) -> Result[int]:
        """"""
        logger.info(msg="Start")
        logger.debug(msg=f"Syncing activities for athlete {athlete_id} - pages {pages}")

        result_token: Result[StravaTokenEntity] = self.auth_service.get_valid_token(athlete_id=athlete_id)

        if result_token.failed:
            logger.error(msg="An error occurred while getting valid token")
            return Result.fail(error=result_token.error)

        all_activities: list[ActivityEntity] = []

        for page in range(1, pages + 1):
            result_activities: Result

        logger.info(msg="End")


