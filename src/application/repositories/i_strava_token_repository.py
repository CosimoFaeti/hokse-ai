from abc import ABC, abstractmethod
from pydantic import UUID4

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result

class IStravaTokenRepository(ABC):

    # region GET
    @staticmethod
    @abstractmethod
    async def get(athlete_id: str) -> Result[StravaTokenEntity]:
        # TODO: id should be athlete_id, think about changing name or data type
        pass
    # endregion

    # region POST
    @staticmethod
    @abstractmethod
    async def post(token: StravaTokenEntity) -> Result[StravaTokenEntity]:
        pass
    # endregion

    # region DELETE
    @staticmethod
    @abstractmethod
    async def delete(athlete_id: str) -> Result[StravaTokenEntity]:
        pass
    # endregion