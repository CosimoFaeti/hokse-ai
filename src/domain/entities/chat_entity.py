import uuid
from pydantic import BaseModel, UUID4, Field


class ChatEntity(BaseModel):
	""""""

	id: UUID4 = Field(title="id", description="Id of the chat", default_factory=uuid.uuid4)

	message: str = Field(title="message", description="AI generated response for the given answer")

	generation_time: float = Field(title="generation_time", description="Message generation time")
