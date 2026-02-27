from pydantic import BaseModel, Field, UUID4

from src.domain.entities.vector_entity import VectorEntity


class PointEntity(BaseModel):
	"""Base entity for Vector database point. This entity will be extended with the appropriate payload in order to
	made up an entity that will be stored on the Vector database.
	"""

	id: UUID4 = Field(title="id", description="Point id")

	vector: list[float] | VectorEntity = Field(title="vector", description="Vector")
