from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	""" """

	PORT: int = Field(title="PORT", description="Port on which the microservice is exposed.", default=8000)

	LOG_LEVEL: Literal["debug", "info", "warning", "error"] = Field(
		title="LOG_LEVEL", description="Level for log display.", default="info"
	)

	# region NOSQL

	NOSQL_DB_HOST: str | None = Field(
		title="NOSQL_DB_HOST", description="Database host for NOSQL database.", default=None
	)

	NOSQL_DB_PORT: int | None = Field(
		title="NOSQL_DB_PORT", description="Database port for NOSQL database.", default=None
	)

	NOSQL_DB_USER: str | None = Field(
		title="NOSQL_DB_USER", description="Database username for NOSQL database.", default=None
	)

	NOSQL_DB_PASSWORD: SecretStr = Field(
		title="NOSQL_DB_PASSWORD", description="Password for NOSQL database.", default=None

	)

	NOSQL_DB_NAME: str | None = Field(
		title="NOSQL_DB_NAME", description="Database name for NOSQL database.", default=None
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

	STRAVA_TOKEN_URL: str | None = Field(
		title="STRAVA_TOKEN_URL", description="Token url for accessing Strava API.", default=None
	)

	STRAVA_API_URL: str | None = Field(
		title="STRAVA_API_URL", description="Base URL for accessing Strava API.", default=None
	)

	STRAVA_REDIRECT_URL: str | None = Field(
		title="STRAVA_REDIRECT_URL", description="Redirect url for accessing Strava API.", default=None
	)

	STRAVA_SCOPE: str | list[str] = Field(
		title="STRAVA_SCOPE", description="Scope for accessing Strava API.", default=None
	)

	# endregion


SETTINGS = Settings(_env_file=".env", _env_file_encoding="utf-8")
