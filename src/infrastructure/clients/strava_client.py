from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton


class StravaClient(metaclass=Singleton):
    """Utility class to manage connection with Strava API."""

    access_token: str | None = None
    refresh_token: str | None = None

    def __init__(self):

        logger.info(msg="Start")



        self.client_id = SETTINGS.STRAVA_CLIENT_ID
        self.client_secret = SETTINGS.STRAVA_CLIENT_SECRET
        self.access_token = self.access_token
        self.refresh_token = self.refresh_token



        logger.info(msg="End")



