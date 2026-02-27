from pydantic import BaseModel, Field


class QueryTemplateInputDTO(BaseModel):
	"""Represents a user query on the templates collection."""

	text: str = Field(title="text", description="Query text.")
