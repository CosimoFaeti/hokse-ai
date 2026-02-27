from pydantic import BaseModel, Field


class PutTemplateInputDTO(BaseModel):
	"""Represents the object passed to a /PUT templates operation."""

	description: str = Field(title="description", description="Entity description")
