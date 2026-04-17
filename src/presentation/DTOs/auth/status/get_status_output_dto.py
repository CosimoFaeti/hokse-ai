from pydantic import BaseModel


class GetStatusOutputDTO(BaseModel):
	athlete_id: int
	access_token: str
	refresh_token: str
	expires_in: int
	scope: str
