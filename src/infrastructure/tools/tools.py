from langchain_core.tools import tools

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.results.result import Result
from src.persistence.repositories.activity_repository import ActivityRepository

@tools
async def get_activities(sport_type: str | None = None, limit: int = 10) -> Result[...]:
    """"""
    result_activities = await ActivityRepository().get(
        sport_type=sport_type,
        limit=limit,
    )

    if result_activities.failed:
        return Result.fail(error=result_activities.error)

    activities: list[ActivityEntity] = result_activities.value
