from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	""" """

	PORT: int = Field(title="PORT", description="Port on which the microservice is exposed.", default=8000)

	PRODUCTION_MODE: bool = Field(
		title="PRODUCTION_MODE", description="Whether to enable or not production mode", default=False
	)

	LOG_LEVEL: Literal["debug", "info", "warning", "error"] = Field(
		title="LOG_LEVEL", description="Level for log display.", default="info"
	)

	# region RELATIONAL_DB

	RELATIONAL_DB_TYPE: str | None = Field(
		title="RELATIONAL_DB_TYPE", description="Type of relational database used.", default=None
	)

	RELATIONAL_DB_HOST: str | None = Field(
		title="RELATIONAL_DB_HOST", description="Host on which the relational database is deployed.", default=None
	)

	RELATIONAL_DB_PORT: str | None = Field(
		title="RELATIONAL_DB_PORT", description="Port on which the relational database is exposed.", default=None
	)

	RELATIONAL_DB_USER: str | None = Field(
		title="RELATIONAL_DB_USER", description="Username for accessing relational database.", default=None
	)

	RELATIONAL_DB_PASSWORD: SecretStr = Field(
		title="RELATIONAL_DB_PASSWORD", description="Password for accessing relational database.", default=None
	)

	RELATIONAL_DB_NAME: str | None = Field(
		title="RELATIONAL_DB_NAME", description="Name of the relational database.", default=None
	)

	# endregion

	# region AI

	GOOGLE_API_KEY: str | None = Field(
		title="GOOGLE_API_KEY", description="Client key for accessing Google API.", default=None
	)

	GEMINI_MODEL: str | None = Field(
		title="GEMINI_MODEL", description="Model for accessing Google API.", default=None
	)

	# endregion

	# region STRAVA

	STRAVA_CLIENT_ID: str | None = Field(
		title="STRAVA_CLIENT_ID", description="Client id for accessing Strava API.", default=None
	)

	STRAVA_CLIENT_SECRET: str | None = Field(
		title="STRAVA_CLIENT_SECRET", description="Client secret for accessing Strava API.", default=None
	)

	STRAVA_OAUTH_URL: str | None = Field(
		title="STRAVA_OAUTH_URL", description="OAuth url for accessing Strava API.", default=None
	)

	STRAVA_API_URL: str | None = Field(
		title="STRAVA_API_URL", description="Base URL for accessing Strava API.", default=None
	)

	# endregion


SETTINGS = Settings(_env_file=".env", _env_file_encoding="utf-8")
