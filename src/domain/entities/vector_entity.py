from pydantic import BaseModel, Field


class VectorEntity(BaseModel):
	"""Represents an array in a compatible manner with Qdrant PointStruct."""

	name: str = Field(title="name", description="Vector name")
	vector: list[float] = Field(title="vector", description="Actual vector")
