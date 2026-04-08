from pydantic import BaseModel


class PostChatInputDTO(BaseModel):
    """"""
    athlete_id: int
    message: str