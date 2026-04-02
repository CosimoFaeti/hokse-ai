from abc import ABC, abstractmethod

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result


class IStravaClient(ABC):

    @abstractmethod
    async def exchange_code(self, code: str) -> Result[StravaTokenEntity]:
        pass

    @abstractmethod
    async def refresh_token(self, token: StravaTokenEntity) -> Result[StravaTokenEntity]:
        pass

    @abstractmethod
    async def get_activities(self, athlete_id: int, per_page: int, page: int) -> Result[list[ActivityEntity]]:
        pass