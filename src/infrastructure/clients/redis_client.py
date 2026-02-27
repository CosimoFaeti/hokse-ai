import redis.asyncio as redis

from src.domain.entities.key_value_entity import KeyValueEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton


class RedisClient(metaclass=Singleton):
	"""
	Utility class to perform basic operations on a Redis database.
	"""

	def __init__(self):
		""" """

		self.client = redis.Redis(
			host=SETTINGS.REDIS_DB_HOST,
			port=SETTINGS.REDIS_DB_PORT,
			username=SETTINGS.REDIS_DB_USER,
			password=SETTINGS.REDIS_DB_PASSWORD.get_secret_value(),
			db=SETTINGS.REDIS_DB_NAME
		)

	@exception_handler
	async def get(self, key: str) -> Result[str]:
		"""
		Retrieve the value associated to the given key.

		:param str key: key for which the value must be retrieved.
		:return: a Result object containing the value associated to the given key, or containing the error in case of
		failure.
		:rtype: Result[str]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: key={key}")

		value = await self.client.get(name=key)

		if value is None:
			logger.error(msg=f"Entry with key={key} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(key=key))

		logger.info(msg="End")
		logger.debug(msg=f"Return value={value}")

		return Result.ok(value=value)

	@exception_handler
	async def set(self, key: str, value: str) -> Result[KeyValueEntity]:
		"""
		Set the value associated to the given key.

		:param str key: key used to retrieve the value.
		:param str value: value that must be saved,
		:return: a Result object containing the value associated to the given key, or containing the error in case of
		failure.
		:rtype: Result[KeyValueEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: key={key}, value={value}")

		await self.client.set(name=key, value=value)

		logger.info(msg="End")
		logger.debug(msg=f"Return value={value}")

		return Result.ok(value=KeyValueEntity(key=key, value=value))
