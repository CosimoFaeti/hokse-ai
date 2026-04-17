from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.auth.revoke.delete_revoke_output_dto import DeleteRevokeOutputDTO


class DeleteRevokeMappers:
	""""""

	@staticmethod
	def to_dto(entity: StravaTokenEntity) -> DeleteRevokeOutputDTO:
		""""""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: DeleteRevokeOutputDTO = DeleteRevokeOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
