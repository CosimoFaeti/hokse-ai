import datetime

from datetime import datetime
from pydantic import BaseModel, Field
from enum import StrEnum


class Activity(BaseModel):
    """ Represents an activity """

    id: int = Field(
        title="id", description="Unique ID for activity."
    )

    athlete_id: int = Field(
        title="athlete_id", description="Unique ID for athlete."
    )

    name: str | None = Field(
        title="name", description="Name of the activity."
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

    sport_type: str | None = Field(
        title="sport_type", description="Type of sport of the activity."
    )

    start_date: datetime | None = Field(
        title="start_date", description="The time at which the activity was started."
    )

class SportType(StrEnum):
    """Represents sport type"""
    RUN = "Run"
    RIDE = "Ride"
    SWIM = "Swim"
    WALK = "Walk"
    HIKE = "Hike"
    WORKOUT = "Workout"
    OTHER = "Other"




    # TODO