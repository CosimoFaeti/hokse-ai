from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.vector.delete_templates_output_dto import DeleteTemplateOutputDTO


class DeleteTemplateMappers:
	"""Mappers to transform VectorDatabaseTemplateEntity into DeleteTemplateOutputDTO, or DeleteTemplateInputDTO into VectorDatabaseTemplateEntity"""

	@staticmethod
	def to_dto(entity: VectorDatabaseTemplateEntity) -> DeleteTemplateOutputDTO:
		"""
		Transforms a VectorDatabaseTemplateEntity object into a DeleteTemplateOutputDTO.

		:param VectorDatabaseTemplateEntity entity: object to be transformed.
		:return: a DeleteTemplateOutputDTO object obtained by the given VectorDatabaseTemplateEntity object.
		:rtype: DeleteTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: DeleteTemplateOutputDTO = DeleteTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
