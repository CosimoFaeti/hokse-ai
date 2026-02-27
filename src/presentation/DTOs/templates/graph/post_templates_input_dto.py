from pydantic import BaseModel, Field


class PostTemplateInputDTO(BaseModel):
	"""Represents the object passed to a /POST templates operation."""

	description: str = Field(title="description", description="Entity description")
