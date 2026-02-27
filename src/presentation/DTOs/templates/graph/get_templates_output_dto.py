from pydantic import UUID4, BaseModel, Field


class GetTemplateOutputDTO(BaseModel):
	"""Represents the object returned by a /GET templates operation."""

	id: UUID4 = Field(title="id", description="Entity id")

	description: str = Field(title="description", description="Entity description")
