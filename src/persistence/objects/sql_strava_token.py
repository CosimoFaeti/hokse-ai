from uuid import uuid4
from pydantic import UUID4
from sqlmodel import SQLModel, Field

from src.domain.entities.strava_token_entity import StravaTokenEntity


class StravaToken(SQLModel, StravaTokenEntity, table=True):
	__tablename__ = "strava_token"

	id: UUID4 = Field(default_factory=uuid4, primary_key=True)
