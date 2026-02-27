from pydantic import BaseModel, Field


class VectorDatabaseTemplatePayloadEntity(BaseModel):
	"""Represents the payload for a document within the ``templates`` collection."""

	text: str = Field(title="text", description="Content of the document")

	upload_date: str = Field(title="upload_date", description="Date in which the document has been uploaded")
