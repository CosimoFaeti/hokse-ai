from src.domain.entities.template_entity import TemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.sql.put_templates_input_dto import PutTemplateInputDTO
from src.presentation.DTOs.templates.sql.put_templates_output_dto import PutTemplateOutputDTO


class PutTemplateMappers:
	"""Mappers to transform TemplateEntity into PutTemplateOutputDTO, or PutTemplateInputDTO into TemplateEntity"""

	@staticmethod
	def to_dto(entity: TemplateEntity) -> PutTemplateOutputDTO:
		"""
		Transforms a TemplateEntity object into a PutTemplateOutputDTO.

		:param TemplateEntity entity: object to be transformed.
		:return: a PutTemplateOutputDTO object obtained by the given TemplateEntity object.
		:rtype: PutTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: PutTemplateOutputDTO = PutTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto

	@staticmethod
	def to_entity(dto: PutTemplateInputDTO) -> TemplateEntity:
		"""
		Transforms a PutTemplateInputDTO object into a TemplateEntity.

		:param PutTemplateInputDTO dto: object to be transformed.
		:return: a TemplateEntity object obtained by the given PutTemplateInputDTO object.
		:rtype: TemplateEntity
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: dto={dto}")

		entity: TemplateEntity = TemplateEntity(**dto.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={entity}")

		return entity
