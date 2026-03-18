import uuid
from pydantic import Field, UUID4
from beanie import Document

from src.domain.entities.activity_entity import ActivityEntity


class Activity(Document, ActivityEntity):
	id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")

	class Settings:
		name = "activity"
