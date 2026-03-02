from pydantic import BaseModel, Field

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