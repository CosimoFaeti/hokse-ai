import uuid

from src.domain.entities.template_entity import TemplateEntity
from beanie import Document
from pydantic import Field, UUID4


class NoSQLTemplate(Document, TemplateEntity):
	id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")

	class Settings:
		name = "templates"
