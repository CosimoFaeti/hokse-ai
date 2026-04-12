from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	""" """

	API_HOST: str = Field(title="HOST", description="Host on which the microservice is running.", default="localhost")

	API_PORT: int = Field(title="PORT", description="Port on which the microservice is exposed.", default=8000)

	API_BASE_URL: str | None = Field(
		title="API_BASE_URL", description="Full base URL for the API (overrides API_HOST+API_PORT, used for deployments like Render).", default=None
	)

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

	LLM_PROVIDER: str = Field(
		title="LLM_PROVIDER", description="Provider for LLM API.", default="google"
	)

	LLM_MODEL: str = Field(
		title="LLM_MODEL", description="Model for accessing LLM API.", default="")

	LLM_API_KEY: str | None = Field(
		title="LLM_API_KEY", description="API key for LLM API.", default=None
	)

	LLM_HOST: str | None = Field(
		title="LLM_HOST", description="Host for LLM API.", default=None
	)

	LLM_PORT: int | None = Field(
		title="LLM_PORT", description="Port for LLM API.", default=None
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

	STRAVA_REDIRECT_URI: str | None = Field(
		title="STRAVA_REDIRECT_URL", description="Redirect url for accessing Strava API.", default=None
	)

	STRAVA_SCOPE: str | list[str] = Field(
		title="STRAVA_SCOPE", description="Scope for accessing Strava API.", default=None
	)

	# endregion

	# region UI

	UI_HOST: str | None = Field(
		title="UI_HOST", description="Host on which the UI is running.", default="localhost"
	)

	UI_PORT: int | None = Field(
		title="UI_PORT", description="Port on which the UI is exposed.", default=8501
	)

	# endregion


SETTINGS = Settings(_env_file=".env", _env_file_encoding="utf-8")
