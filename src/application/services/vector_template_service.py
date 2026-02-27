from typing import Type

from src.application.clients.i_langchain_client import ILangchainClient
from src.application.interfaces.i_vector_template_service import IVectorTemplateService
from src.application.repositories.i_vector_template_repository import IVectorTemplateRepository
from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.infrastructure.clients.langchain_client import LangchainClient
from src.persistence.repositories.vector_template_repository import VectorTemplateRepository
from pydantic import UUID4


class VectorTemplateService(IVectorTemplateService):
	"""
	Forwards requests to Vector database repository and Langchain client.
	"""

	def __init__(self, repository: Type[IVectorTemplateRepository], langchain_client: ILangchainClient):
		self.repository = repository
		self.langchain_client = langchain_client

	# region POST
	@exception_handler
	async def post(self, text: str) -> Result[list[VectorDatabaseTemplateEntity]]:
		"""
		Create embeddings for the given entity.

		:param
		:return: a Result object containing the list of points inserted within the Vector database if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[list[VectorDatabaseTemplateEntity]]
		"""

		logger.info(msg="Start")

		embedding_result: Result[list[VectorDatabaseTemplateEntity]] = await self.langchain_client.embed(text=text)

		if embedding_result.failed:
			logger.error(msg="An error occurred while computing the embeddings.")
			return Result.fail(error=embedding_result.error)

		for chunk in embedding_result.value:
			await self.repository.post(entity=chunk)

		logger.info(msg="End")

		return embedding_result

	# endregion

	# region DELETE
	@exception_handler
	async def delete(self, id: UUID4) -> Result[VectorDatabaseTemplateEntity]:
		"""
		Delete the point whose id is passed as parameter from the Vector database.

		:param UUID4 id: id of the point to be deleted.
		:return: a Result object containing the deleted point if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[VectorDatabaseTemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[VectorDatabaseTemplateEntity] = await self.repository.delete(id=id)

		logger.info(msg="End")

		return result

	# endregion

	# region QUERY
	@exception_handler
	async def query(self, text: str) -> Result[list[VectorDatabaseTemplateEntity]]:
		"""
		Query Vector database for points similar to the given query.

		:param str text: query.
		:return: a Result object containing the list of points related to the given query if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[list[VectorDatabaseTemplateEntity]]
		"""

		logger.info(msg="Start")

		embedding_result: Result[list[VectorDatabaseTemplateEntity]] = await self.langchain_client.embed(text=text)

		if embedding_result.failed:
			logger.error(msg="An error occurred while computing the embeddings.")
			return Result.fail(error=embedding_result.error)

		query_vector: list[float] = embedding_result.value[0].vector

		result: Result[list[VectorDatabaseTemplateEntity]] = await self.repository.query(vector=query_vector)

		logger.info(msg="End")

		return result

	# endregion
