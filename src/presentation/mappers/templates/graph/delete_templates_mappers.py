from src.domain.entities.template_entity import TemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.nosql.delete_templates_output_dto import DeleteTemplateOutputDTO


class DeleteTemplateMappers:
	"""Mappers to transform TemplateEntity into DeleteTemplateOutputDTO, or DeleteTemplateInputDTO into TemplateEntity."""

	@staticmethod
	def to_dto(entity: TemplateEntity) -> DeleteTemplateOutputDTO:
		"""
		Transforms a TemplateEntity object into a DeleteTemplateOutputDTO.

		:param TemplateEntity entity: object to be transformed.
		:return: a DeleteTemplateOutputDTO object obtained by the given TemplateEntity object.
		:rtype: DeleteTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: DeleteTemplateOutputDTO = DeleteTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
