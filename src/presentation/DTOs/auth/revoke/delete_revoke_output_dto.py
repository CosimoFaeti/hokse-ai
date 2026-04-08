from pydantic import BaseModel


class DeleteRevokeOutputDTO(BaseModel):
    athlete_id: int
    access_token: str
    refresh_token: str
    expires_in: int
    scope: str