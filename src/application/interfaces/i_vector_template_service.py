from abc import ABC, abstractmethod
from pydantic import UUID4
from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.results.result import Result


class IVectorTemplateService(ABC):

	# region POST
	@staticmethod
	@abstractmethod
	async def post(text: str) -> Result[list[VectorDatabaseTemplateEntity]]:
		"""
		Create embeddings for the given entity.

		:param
		:return: a Result object containing the list of points inserted within the Vector database if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[list[VectorDatabaseTemplateEntity]]
		"""

		pass

	# endregion

	# region DELETE
	@staticmethod
	@abstractmethod
	async def delete(id: UUID4) -> Result[VectorDatabaseTemplateEntity]:
		"""
		Delete the point whose id is passed as parameter from the Vector database.

		:param UUID4 id: id of the point to be deleted.
		:return: a Result object containing the deleted point if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[VectorDatabaseTemplateEntity]
		"""

		pass

	# endregion

	# region QUERY
	@staticmethod
	@abstractmethod
	async def query(text: str) -> Result[list[VectorDatabaseTemplateEntity]]:
		"""
		Query Vector database for points similar to the given query.

		:param str text: query.
		:return: a Result object containing the list of points related to the given query if the operation has
		been successful, a Result object containing the error if the operation failed.
		:rtype: Result[list[VectorDatabaseTemplateEntity]]
		"""

		pass
