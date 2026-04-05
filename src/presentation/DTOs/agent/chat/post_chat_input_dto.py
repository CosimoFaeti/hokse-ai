from pydantic import BaseModel, Field


class PostChatInputDTO(BaseModel):
    """"""
    athlete_id: int
    message: str