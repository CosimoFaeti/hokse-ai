from src.domain.entities.chat_entity import ChatEntity
from src.domain.utilities.logger import logger
from src.presentation.DTOs.agent.chat.post_chat_output_dto import PostChatOutputDTO


class PostChatMappers:
	""""""

	@staticmethod
	def to_dto(entity: ChatEntity) -> PostChatOutputDTO:
		""""""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		dto: PostChatOutputDTO = PostChatOutputDTO(**entity.model_dump())

		logger.info(msg="End")
		logger.debug(msg=f"Return value={dto}")

		return dto