from pydantic import BaseModel, Field


class KeyValueEntity(BaseModel):
	"""Represents a key-value pair in which both key and value are bound to be strings."""

	key: str = Field(
		title="key",
		description="Entity key",
	)

	value: str = Field(title="value", description="Entity value")
