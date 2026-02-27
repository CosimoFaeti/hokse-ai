from abc import ABC, abstractmethod
from pydantic import UUID4
from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.results.result import Result


class IVectorTemplateRepository(ABC):

	# region POST
	@staticmethod
	@abstractmethod
	async def post(entity: VectorDatabaseTemplateEntity) -> Result[VectorDatabaseTemplateEntity]:
		"""
		Insert a new point into the associated Vector database collection.

		:param entity:
		:return:
		:rtype: Result[
		"""

		pass

	# endregion

	# region DELETE

	@staticmethod
	@abstractmethod
	async def delete(id: UUID4) -> Result[VectorDatabaseTemplateEntity]:
		""" """

		pass

	# endregion

	# region QUERY
	@staticmethod
	@abstractmethod
	async def query(
			vector: list[float], limit: int = 10, score_threshold: float | None = None
	) -> Result[list[VectorDatabaseTemplateEntity]]:
		""" """

		pass

# endregion