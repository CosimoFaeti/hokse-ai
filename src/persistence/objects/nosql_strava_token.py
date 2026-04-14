import uuid
from datetime import datetime, timezone
from pydantic import Field, UUID4
from beanie import Document

from src.domain.entities.strava_token_entity import StravaTokenEntity


class StravaToken(Document, StravaTokenEntity):
	id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")
	upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

	class Settings:
		name = "strava_token"
