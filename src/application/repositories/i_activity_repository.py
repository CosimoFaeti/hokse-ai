from abc import ABC, abstractmethod

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.results.result import Result


class IActivityRepository(ABC):

    # region GET
    @staticmethod
    @abstractmethod
    async def get(athlete_id: int, sport_type: str | None = None, limit: int = 10, start: str | None = None, end: str | None = None) -> Result[list[ActivityEntity]]:
        pass
    # endregion

    # region POST
    @staticmethod
    @abstractmethod
    async def post(activities: list[ActivityEntity]) -> Result[list[ActivityEntity]]:
        pass
    # endregion