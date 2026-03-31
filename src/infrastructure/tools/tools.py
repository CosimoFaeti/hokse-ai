import datetime
from datetime import datetime, timezone, timedelta
from langchain_core.tools import tools

from src.domain.entities.activity_entity import ActivityEntity
from src.domain.results.result import Result
from src.domain.utilities.constants import PERIODS
from src.infrastructure.utils.tools_helpers import resolve_period, prev_numeric, format_delta, overall_trend, stats, _row
from src.persistence.repositories.activity_repository import ActivityRepository

@tools
async def get_activities(athlete_id: int, mode: str = "list", sport_type: str | None = "Run", limit: int = 10, period: str | None = None) -> Result[str]:
    """"""
    if mode == "list":

        result_activities = await ActivityRepository().get(
            athlete_id=athlete_id,
            sport_type=sport_type,
            limit=limit,
        )

        if result_activities.failed:
            return Result.fail(error=result_activities.error)

        activities: list[ActivityEntity] = result_activities.value

        lines: list[str] = []
        for a in activities:
            date_str: str = a.start_date.strftime("%Y-%m-%d")
            pace_str: str = (
                f" | {a.pace_min_per_km:.2f} min/km"
                if a.pace_min_per_km and a.sport_type == "Run"
                else ""
            )
            hr_str: str = (
                f" | HR {a.average_heartrate:.0f} bpm"
                if a.average_heartrate
                else ""
            )
            elev_str: str = (
                f" | +{a.total_elevation_gain:.0f} m"
                if a.total_elevation_gain > 0
                else ""
            )
            lines.append(
                f"[{date_str}] {a.sport_type}: {a.name}"
                f" - {a.distance_km:.1f} km"
                f" in {a.moving_time_minutes:.0f} min"
                f"{pace_str} in {hr_str} in {elev_str}"
            )
        return "\n".join(lines)
    elif mode == "aggregate":
        now: datetime = datetime.now(tz=timezone.utc)
        start, end = resolve_period(period, now)

        result_activities = await ActivityRepository().get(
            athlete_id=athlete_id,
            sport_type=sport_type,
            limit=limit,
            start=start.isoformat(),
            end=end.isoformat(),
        )

        if result_activities.failed:
            return Result.fail(error=result_activities.error)

        activities: list[ActivityEntity] = result_activities.value

        total_km = sum(a.distance_km for a in activities)
        total_min = sum(a.moving_time_minutes for a in activities)
        total_elev = sum(a.total_elevation_gain for a in activities)
        hr_readings = [a.average_heartrate for a in activities if a.average_heartrate]
        avg_hr = sum(hr_readings) / len(hr_readings) if hr_readings else None
        hr_lines = f"\n Avg heart rate : {avg_hr:.0f} bpm" if avg_hr else ""

        return (
            f"Stats - {period}:\n"
            f"Activities: {len(activities)}\n"
            f"Total distance: {total_km:.1f} km\n"
            f"Total time: {total_min:.0f} min ({total_min / 60:.1f} h)\n"
            f"Total elevation: {total_elev:.0f} m"
            f"{hr_lines}"
        )