from motor.motor_asyncio import AsyncIOMotorClient

from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton

from beanie import init_beanie


class NoSQLDatabaseManager(metaclass=Singleton):
	"""
	Utility class to manage connection to NoSQL database connection.
	"""

	def __init__(self):
		"""
		Initialize the connection to NoSQL database.
		"""

		logger.info(msg="Start")
		logger.debug(
			msg=f"Connecting to mongodb://{SETTINGS.NOSQL_DB_USER}:{SETTINGS.NOSQL_DB_PASSWORD}@{SETTINGS.NOSQL_DB_HOST}:{SETTINGS.NOSQL_DB_PORT}"
		)

		self.async_client = AsyncIOMotorClient(
			f"mongodb://{SETTINGS.NOSQL_DB_USER}:{SETTINGS.NOSQL_DB_PASSWORD.get_secret_value()}@{SETTINGS.NOSQL_DB_HOST}:{SETTINGS.NOSQL_DB_PORT}"
		)

		logger.info(msg="End")

	async def create_collections(self) -> None:
		"""
		Create NoSQL database collections.
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Trying to create tables on database {self.async_client[SETTINGS.NOSQL_DB_NAME]}")
		# Initialize beanie with the Product document class
		await init_beanie(
			self.async_client[SETTINGS.NOSQL_DB_NAME],
			document_models=["src.persistence.objects.nosql_template.NoSQLTemplate"],
		)

		logger.info(msg="End")

	def get_session(self):
		""" """

		return self.async_client.start_session()
