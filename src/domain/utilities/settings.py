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

	# region VECTOR_DB

	VECTOR_DB_HOST: str | None = Field(
		title="VECTOR_DB_HOST", description="Host on which the vector database is deployed.", default=None
	)

	VECTOR_DB_PORT: str | None = Field(
		title="VECTOR_DB_PORT", description="Port on which the vector database is exposed.", default=None
	)

	VECTOR_DB_APIKEY: SecretStr = Field(
		title="VECTOR_DB_APIKEY", description="Api key for accessing vector database.", default=None
	)

	VECTOR_DB_COLLECTION_NAME: str | None = Field(
		title="VECTOR_DB_COLLECTION_NAME",
		description="Name of the collection used in the vector database.",
		default=None,
	)

	# endregion

	# region KEY_VALUE_DB

	REDIS_DB_HOST: str = Field(
		title="REDIS_DB_HOST", description="Host on which the Redis database is deployed."
	)

	REDIS_DB_USER: str = Field(
		title="REDIS_DB_USER", description="Username for accessing Redis database."
	)

	REDIS_DB_PASSWORD: SecretStr = Field(
		title="REDIS_DB_PASSWORD", description="Password for accessing Redis database."
	)

	REDIS_DB_PORT: int = Field(
		title="REDIS_DB_PORT", description="Port on which the Redis database is exposed."
	)

	REDIS_DB_NAME: int = Field(
		title="REDIS_DB_NAME", description="Name of the relational database."
	)

	# endregion

	# region NOSQL

	NOSQL_DB_HOST: str | None = Field()

	NOSQL_DB_PORT: int | None = Field()

	NOSQL_DB_USER: str | None = Field()

	NOSQL_DB_PASSWORD: SecretStr = Field()

	NOSQL_DB_NAME: str | None = Field()

	# endregion

	# region GRAPH

	GRAPH_DB_HOST: str | None = Field()
	GRAPH_DB_PORT: int = Field()
	GRAPH_DB_USER: str = Field()
	GRAPH_DB_PASSWORD: SecretStr = Field()

	# endregion

	# region AI

	EMBEDDER_HOST: str | None = Field(
		title="EMBEDDER_HOST", description="Host on which the embedder is deployed.", default=None
	)

	EMBEDDER_PORT: int | None = Field(
		title="EMBEDDER_PORT", description="Port on which the embedder is exposed.", default=None
	)

	EMBEDDER_NAME: str | None = Field(title="EMBEDDER_NAME", description="Name of the embedder.", default=None)

	# endregion


SETTINGS = Settings(_env_file=".env", _env_file_encoding="utf-8")
