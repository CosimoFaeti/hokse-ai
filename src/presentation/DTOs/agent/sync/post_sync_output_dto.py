from datetime import datetime
from pydantic import BaseModel


class PostSyncOutputDTO(BaseModel):
    """"""
    athlete_id: int
    name: str | None
    sport_type: str | None
    distance: float | None
    moving_time: int | None
    elapsed_time: int | None
    total_elevation_gain: float | None
    elev_high: float | None
    elev_low: float | None
    average_heart_rate: float | None
    start_date: datetime | None