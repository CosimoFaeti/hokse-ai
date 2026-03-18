from typing import List
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, field_validator


class StravaTokenEntity(BaseModel):
    """Represents Strava response token"""

    athlete_id: int | None = Field(
        title="strava_athlete_id", description="Strava athlete id for Strava API."
    )

    access_token: str | None = Field(
        title="access_token", description="Access token for Strava API."
    )

    refresh_token: str | None = Field(
        title="refresh_token", description="Refresh token for Strava API."
    )

    expires_at: int | None = Field(
        title="expires_at", description="Expiration time for Strava API."
    )

    scope: str | List[str] = Field(
        title="scope", description="Scopes for Strava API."
    )

    @field_validator('expires_at', mode='before')
    @classmethod
    def parse_timestamp(cls, v: int | datetime) -> datetime:
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

    def is_expired(self) -> bool:
        return datetime.now(tz=timezone.utc) >= self.expires_at

    def refresh(self, buffer_seconds: int) -> bool:
        threshold = datetime.now(tz=timezone.utc) + timedelta(seconds=buffer_seconds)
        return threshold >= self.expires_at