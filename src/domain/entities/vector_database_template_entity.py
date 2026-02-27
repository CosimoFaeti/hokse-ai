from src.domain.entities.point_entity import PointEntity
from pydantic import Field

from src.domain.entities.vector_database_template_payload_entity import VectorDatabaseTemplatePayloadEntity


class VectorDatabaseTemplateEntity(PointEntity):
	"""Represents the object stored within the ``templates`` collection within the Vector database."""

	payload: VectorDatabaseTemplatePayloadEntity = Field(
		title="payload", description="Payload for the entity within the 'templates' collection"
	)
