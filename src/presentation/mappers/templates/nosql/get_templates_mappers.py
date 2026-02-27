from src.domain.entities.template_entity import TemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.nosql.get_templates_output_dto import GetTemplateOutputDTO


class GetTemplateMappers:
	"""Mappers to transform TemplateEntity into GetTemplateOutputDTO, or GetTemplateInputDTO into TemplateEntity."""

	@staticmethod
	def to_dto(entity: TemplateEntity) -> GetTemplateOutputDTO:
		"""
		Transforms a TemplateEntity object into a GetTemplateOutputDTO.

		:param TemplateEntity entity: object to be transformed.
		:return: a GetTemplateOutputDTO object obtained by the given TemplateEntity object.
		:rtype: GetTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: GetTemplateOutputDTO = GetTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
