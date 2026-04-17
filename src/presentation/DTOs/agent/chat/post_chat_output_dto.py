from pydantic import BaseModel, UUID4


class PostChatOutputDTO(BaseModel):
	""""""

	id: UUID4
	message: str
	generation_time: float
