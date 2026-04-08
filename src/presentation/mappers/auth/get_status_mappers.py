from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.auth.status.get_status_output_dto import GetStatusOutputDTO


class GetStatusMappers:
	""""""

	@staticmethod
	def to_dto(entity: StravaTokenEntity) -> GetStatusOutputDTO:
		""""""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: GetStatusOutputDTO = GetStatusOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto