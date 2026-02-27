from src.domain.entities.template_entity import TemplateEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.templates.sql.post_templates_input_dto import PostTemplateInputDTO
from src.presentation.DTOs.templates.sql.post_templates_output_dto import PostTemplateOutputDTO


class PostTemplateMappers:
	"""Mappers to transform TemplateEntity into PostTemplateOutputDTO, or PostTemplateInputDTO into TemplateEntity"""

	@staticmethod
	def to_dto(entity: TemplateEntity) -> PostTemplateOutputDTO:
		"""
		Transforms a TemplateEntity object into a PostTemplateOutputDTO.

		:param TemplateEntity entity: object to be transformed.
		:return: a PostTemplateOutputDTO object obtained by the given TemplateEntity object.
		:rtype: PostTemplateOutputDTO
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: PostTemplateOutputDTO = PostTemplateOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto

	@staticmethod
	def to_entity(dto: PostTemplateInputDTO) -> TemplateEntity:
		"""
		Transforms a PostTemplateInputDTO object into a TemplateEntity.

		:param PostTemplateInputDTO dto: object to be transformed.
		:return: a TemplateEntity object obtained by the given PostTemplateInputDTO object.
		:rtype: TemplateEntity
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: dto={dto}")

		entity: TemplateEntity = TemplateEntity(**dto.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return entity
