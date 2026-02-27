from src.domain.entities.template_entity import TemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.nosql.patch_templates_output_dto import PatchTemplateOutputDTO


class PatchTemplateMappers:
	"""Mappers to transform TemplateEntity into PatchTemplateOutputDTO, or PatchTemplateInputDTO into TemplateEntity"""

	@staticmethod
	def to_dto(entity: TemplateEntity) -> PatchTemplateOutputDTO:
		"""
		Transforms a TemplateEntity object into a PatchTemplateOutputDTO.

		:param TemplateEntity entity: object to be transformed.
		:return: a PatchTemplateOutputDTO object obtained by the given TemplateEntity object.
		:rtype: PatchTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: PatchTemplateOutputDTO = PatchTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
