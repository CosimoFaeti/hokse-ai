from datetime import datetime

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.objects.nosql_activity import Activity


class ActivityRepository:
    """Repository to perform operations on activity NoSQL collection."""

    # region GET
    @exception_handler
    @staticmethod
    async def get(athlete_id: int | None, sport_type: str | None = None, limit: int = 10, start: str | None = None, end: str | None = None) -> Result[list[ActivityEntity]]:
        """"""

        logger.info(msg="Start")

        result = Activity.find(Activity.athlete_id == athlete_id)

        if sport_type:
            result = result.find(Activity.sport_type == sport_type)

        if start and end:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            result = result.find(
                Activity.start_date >= start_dt,
                Activity.start_date <= end_dt,
            )

        if result is None:
            logger.error(msg=f"Entry of type activity with key={athlete_id} does not exist.")
            return Result.fail(error=GenericErrors.not_found_error(type="activity", key=str(athlete_id)))

        logger.info(msg="End")

        docs = await result.sort(-Activity.start_date).limit(limit).to_list()

        activities: list[ActivityEntity] = [ActivityEntity(**doc.model_dump()) for doc in docs]

        return Result.ok(value=activities)

    # endregion

    # region POST
    @exception_handler
    @staticmethod
    async def post(activities: list[ActivityEntity]) -> Result[list[ActivityEntity]]:
        """"""

        logger.info(msg="Start")

        docs = [Activity(**activity.model_dump()) for activity in activities]

        await Activity.insert_many(docs)

        logger.info(msg="End")

        return Result.ok(value=activities)

    # endregion
