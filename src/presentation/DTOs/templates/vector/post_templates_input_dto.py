from pydantic import BaseModel, Field


class PostTemplateInputDTO(BaseModel):
	"""Represents the input DTO for creating embeddings and putting them into the templates collection."""

	text: str = Field(title="text", description="Text for which embeddings must be computed.")
