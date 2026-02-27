from pydantic import BaseModel, Field, UUID4


class PostTemplateOutputDTO(BaseModel):
	"""Represents the object returned by a /POST templates operation."""

	id: UUID4 = Field(title="id", description="Entity id")

	description: str = Field(title="description", description="Entity description")
