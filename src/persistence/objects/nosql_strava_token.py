import uuid
from pydantic import Field, UUID4
from beanie import Document

from src.domain.entities.strava_token_entity import StravaTokenEntity


class StravaToken(Document, StravaTokenEntity):
	id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")

	class Settings:
		name = "strava_token"
