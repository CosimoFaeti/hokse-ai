from datetime import datetime
from pydantic import BaseModel


class PostSyncOutputDTO(BaseModel):
	""""""

	athlete_id: int
	name: str | None = None
	sport_type: str | None = None
	distance: float | None = None
	moving_time: int | None = None
	elapsed_time: int | None = None
	total_elevation_gain: float | None = None
	elev_high: float | None = None
	elev_low: float | None = None
	average_heartrate: float | None = None
	start_date: datetime | None = None
