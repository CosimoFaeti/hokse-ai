from src.domain.entities.patch_entity import PatchEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.generic.patch_dto import PatchDTO


class PatchMappers:
	"""
	Mappers to transform PatchDTO into PatchEntity, and vice versa.
	"""

	@staticmethod
	def to_entity(dto: PatchDTO) -> PatchEntity:
		"""
		Transforms a PatchDTO object into a PatchEntity.

		:param PatchDTO dto: object to be transformed.
		:return: a PatchEntity object obtained by the given PatchDTO object.
		:rtype: PatchEntity
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: dto={dto}")

		entity: PatchEntity = PatchEntity(**dto.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={entity}")

		return entity
