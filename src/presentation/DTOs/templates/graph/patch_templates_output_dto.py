from pydantic import BaseModel, UUID4, Field


class PatchTemplateOutputDTO(BaseModel):
	"""Represents the object returned by a /PATCH templates operation."""

	id: UUID4 = Field(title="id", description="Entity id")

	description: str = Field(title="description", description="Entity description")
