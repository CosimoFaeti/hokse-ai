from datetime import datetime
from pydantic import BaseModel, Field


class ActivityEntity(BaseModel):
    """ Represents an activity """

    athlete_id: int | None = Field(
        title="athlete_id", description="Unique ID for athlete."
    )

    name: str | None = Field(
        title="name", description="Name of the activity."
    )

    sport_type: str | None = Field(
        title="sport_type", description="Type of sport of the activity.", default="Run"
    )

    distance: float | None = Field(
        title="distance", description="Distance of the activity, in meters."
    )

    moving_time: int | None = Field(
        title="moving_time", description="Moving time of the activity, in seconds."
    )

    elapsed_time: int | None = Field(
        title="elapsed_time", description="Elapsed time of the activity, in seconds."
    )

    total_elevation_gain: float | None = Field(
        title="total_elevation_gain", description="Total elevation gain of the activity."
    )

    elev_high: float | None = Field(
        title="elev_high", description="Highest elevation of the activity, in meters."
    )

    elev_low: float | None = Field(
        title="elev_low", description="Lowest elevation of the activity, in meters."
    )

    average_heartrate: float | None = Field(
        title="average_heartrate", description="Average heartrate of the activity."
    )

    start_date: datetime | None = Field(
        title="start_date", description="The time at which the activity was started."
    )

    @property
    def distance_km(self) -> float:
        return round(self.distance / 1000, 2)

    @property
    def moving_time_minutes(self) -> float:
        return round(self.moving_time / 60, 1)

    @property
    def pace_min_per_km(self) -> float | None:
        if self.distance == 0:
            return None
        pace_sec = self.moving_time / (self.distance / 1000)
        return round(pace_sec / 60, 2)
