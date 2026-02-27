from pydantic import BaseModel, Field, PastDatetime


class TemplatePayloadDTO(BaseModel):
	"""Represents the input DTO for creating embeddings and putting them into the templates collection."""

	upload_date: PastDatetime = Field(title="upload_date", description="Date in which document has been uploaded.")

	text: str = Field(title="text", description="Text content.")
