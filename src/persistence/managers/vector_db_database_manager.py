from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton
import qdrant_client
from qdrant_client.models import CollectionsResponse, Distance, VectorParams
import httpx


class VectorDBDatabaseManager(metaclass=Singleton):
	"""
	Utility class to manage Vector database connection.

	:param AsyncQdrantClient async_client: asynchronous Qdrant client.
	:param QdrantClient sync_client: synchronous Qdrant client.
	"""

	def __init__(self):
		"""
		Initialize Vector database synchronous and asynchronous clients.
		"""

		self.async_client = qdrant_client.AsyncQdrantClient(
			location=SETTINGS.VECTOR_DB_HOST,
			port=SETTINGS.VECTOR_DB_PORT,
			api_key=SETTINGS.VECTOR_DB_APIKEY.get_secret_value(),
			timeout=10,
			https=SETTINGS.PRODUCTION_MODE,
		)

		self.sync_client = qdrant_client.QdrantClient(
			location=SETTINGS.VECTOR_DB_HOST,
			port=SETTINGS.VECTOR_DB_PORT,
			api_key=SETTINGS.VECTOR_DB_APIKEY.get_secret_value(),
			timeout=10,
			https=SETTINGS.PRODUCTION_MODE,
		)

	def health_check(self):
		# Use the `http` attribute to make a raw HTTP request to the /health endpoint
		response = httpx.get(url=f"{self.sync_client.http.client.host}/healthz")

		if response.status_code == 200:
			logger.info(msg="Qdrant is healthy")
			return

		logger.error(msg="Qdrant is not healthy")
		raise Exception

	def get_async_client(self) -> qdrant_client.AsyncQdrantClient:
		"""
		Retrieve an asynchronous Vector database client to perform operations on the Vector database.

		:return: An asynchronous client to make operations on the Vector database.
		:rtype: AsyncQdrantClient
		"""

		logger.info(msg="Start")

		return self.async_client

	def get_sync_client(self) -> qdrant_client.QdrantClient:
		"""
		Retrieve a synchronous Vector database client to perform operations on the Vector database.

		:return: A synchronous client to make operations on the Vector database.
		:rtype: QdrantClient
		"""

		logger.debug(msg="Start")

		return self.sync_client

	async def create_collection(self, collection_name: str):
		""" """

		logger.info(msg="Start")

		collections: CollectionsResponse = await self.async_client.get_collections()

		if collection_name not in [collection.name for collection in collections.collections]:
			logger.warn(msg=f"Collection {collection_name} does not exist. Creating the collection.")
			await self.async_client.create_collection(
				collection_name=collection_name,
				vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
			)

		logger.info(msg="End")

	@staticmethod
	def get_collection(type: str) -> str:
		"""
		Return the collection related to the given type.

		:param str type: object type, as string.
		:return: the name of the collection related to the given type.
		:rtype: str
		"""

		logger.debug(msg="Start")

		match type:
			case "VectorDatabaseTemplateEntity":
				return SETTINGS.VECTOR_DB_COLLECTION_NAME
			case _:
				return ""
