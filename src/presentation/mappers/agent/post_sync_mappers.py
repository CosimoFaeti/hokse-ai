from src.domain.entities.activity_entity import ActivityEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.agent.sync.post_sync_output_dto import PostSyncOutputDTO


class PostSyncMappers:
	""""""

	@staticmethod
	def to_dto(entity: ActivityEntity) -> PostSyncOutputDTO:
		""""""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: PostSyncOutputDTO = PostSyncOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto
