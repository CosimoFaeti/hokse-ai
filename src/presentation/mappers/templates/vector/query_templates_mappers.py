from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.vector.query_templates_output_dto import QueryTemplateOutputDTO


class QueryTemplateMappers:
	"""Mappers to transform VectorDatabaseTemplateEntity into QueryTemplateOutputDTO, or QueryTemplateInputDTO into VectorDatabaseTemplateEntity"""

	@staticmethod
	def to_dto(entity: VectorDatabaseTemplateEntity) -> QueryTemplateOutputDTO:
		"""
		Transforms a VectorDatabaseTemplateEntity object into a QueryTemplateOutputDTO.

		:param VectorDatabaseTemplateEntity entity: object to be transformed.
		:return: a QueryTemplateOutputDTO object obtained by the given VectorDatabaseTemplateEntity object.
		:rtype: QueryTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: QueryTemplateOutputDTO = QueryTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
