from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.entities.vector_database_template_payload_entity import VectorDatabaseTemplatePayloadEntity
from src.domain.entities.vector_entity import VectorEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.managers.vector_db_database_manager import VectorDBDatabaseManager
from qdrant_client.models import PointStruct
from pydantic import UUID4
from qdrant_client.models import ScoredPoint, Record


class VectorTemplateRepository:
	"""
	Utility class to perform basic operations on Vector Database collection.
	"""

	# region POST
	@exception_handler
	@staticmethod
	async def post(entity: VectorDatabaseTemplateEntity) -> Result[VectorDatabaseTemplateEntity]:
		"""
		Insert a new point into the associated Vector database collection.

		:param entity:
		:return:
		:rtype: Result[
		"""

		logger.info(msg="Start")

		point: PointStruct = PointStruct(
			id=str(entity.id),
			vector={entity.vector.name: entity.vector.vector}
			if isinstance(entity.vector, VectorEntity)
			else entity.vector,
			payload=entity.payload.model_dump(),
		)

		await (
			VectorDBDatabaseManager()
			.get_async_client()
			.upsert(
				collection_name=VectorDBDatabaseManager().get_collection(VectorDatabaseTemplateEntity.__name__),
				wait=True,
				points=[point],
			)
		)

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region DELETE

	@exception_handler
	@staticmethod
	async def delete(id: UUID4) -> Result[VectorDatabaseTemplateEntity]:
		""" """

		logger.info(msg="End")

		points: list[Record] = (
			await VectorDBDatabaseManager()
			.get_async_client()
			.retrieve(
				collection_name=VectorDBDatabaseManager().get_collection(VectorDatabaseTemplateEntity.__name__),
				ids=[str(id)],
				with_vectors=True,
			)
		)

		if len(points) == 0:
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(key=id, type="template"))

		point: Record = points[0]

		await (
			VectorDBDatabaseManager()
			.get_async_client()
			.delete(
				collection_name=VectorDBDatabaseManager().get_collection(VectorDatabaseTemplateEntity.__name__),
				points_selector=[str(id)],
			)
		)

		entity: VectorDatabaseTemplateEntity = VectorDatabaseTemplateEntity(
			id=point.id, vector=point.vector, payload=VectorDatabaseTemplatePayloadEntity(**point.payload)
		)

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region QUERY
	@exception_handler
	@staticmethod
	async def query(
		vector: list[float], limit: int = 10, score_threshold: float | None = None
	) -> Result[list[VectorDatabaseTemplateEntity]]:
		""" """

		logger.info(msg="Start")

		hits: list[ScoredPoint] = await VectorDBDatabaseManager().async_client.search(
			collection_name=VectorDBDatabaseManager().get_collection(VectorDatabaseTemplateEntity.__name__),
			query_vector=vector,
			limit=limit,
			score_threshold=score_threshold,
			with_vectors=True,
		)

		result: list[VectorDatabaseTemplateEntity] = [
			VectorDatabaseTemplateEntity(
				id=hit.id, vector=hit.vector, payload=VectorDatabaseTemplatePayloadEntity(**hit.payload)
			)
			for hit in hits
		]

		logger.info(msg="End")

		return Result.ok(value=result)

	# endregion
