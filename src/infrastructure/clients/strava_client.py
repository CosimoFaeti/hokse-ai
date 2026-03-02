import httpx

from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton


class StravaClient(metaclass=Singleton):
    """Utility class to manage connection with Strava API."""

    def __init__(self, access_token: str):

        logger.info(msg="Start")



        logger.info(msg="End")

