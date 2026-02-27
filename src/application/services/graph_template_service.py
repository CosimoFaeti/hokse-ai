from typing import Type

from pydantic import UUID4

from src.application.repositories.i_graph_template_repository import IGraphTemplateRepository
from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.repositories.graph_template_repository import GraphTemplateRepository


class GraphTemplateService:
	"""
	Utility class to forward API request to the appropriate GraphDB persistence or infrastructure function, as well as
	implementing some logic.
	"""

	def __init__(self, repository: Type[IGraphTemplateRepository]):
		self.repository = repository

	# region POST
	@exception_handler
	async def post(self, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Create a new template.

		:param TemplateEntity entity: template to be created.
		:return: a Result object containing the created entity if operation has been successful, a Result object
		containing the error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[TemplateEntity] = await self.repository.post(entity=entity)

		logger.info(msg="End")

		return result

	# endregion

	# region GET
	@exception_handler
	async def get(self, id: UUID4) -> Result[TemplateEntity]:
		"""
		Retrieve a template from its id.

		:param UUID4 id: id of the template to be retrieved.
		:return: a Result object containing the retrieved entity if operation has been successful, a Result object
		containing the error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[TemplateEntity] = await self.repository.get(id=id)

		logger.info(msg="End")

		return result

	# endregion

	# region DELETE
	@exception_handler
	async def delete(self, id: UUID4) -> Result[TemplateEntity]:
		"""
		Delete a template from its id.

		:param UUID4 id: id of the template to be deleted.
		:return: a Result object containing the deleted entity if operation has been successful, a Result object
		containing the error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[TemplateEntity] = await self.repository.delete(id=id)

		logger.info(msg="End")

		return result

	# endregion

	# region PUT
	@exception_handler
	async def put(self, id: UUID4, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Update a template from its id and the given entity.

		:param UUID4 id: id of the template to be updated.
		:param TemplateEntity entity: entity with which the old entry will be overwritten.
		:return: a Result object containing the retrieved entity if operation has been successful, a Result object
		containing the error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[TemplateEntity] = await self.repository.put(id=id, entity=entity)

		logger.info(msg="End")

		return result

	# endregion

	# region PATCH
	@exception_handler
	async def patch(self, id: UUID4, patches: list[PatchEntity]) -> Result[TemplateEntity]:
		"""
		Patch a template from its id and the given entity.

		:param UUID4 id: id of the template to be updated.
		:param list[PatchEntity] patches: patches to be applied to the entry.
		:return: a Result object containing the retrieved entity if operation has been successful, a Result object
		containing the error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result: Result[TemplateEntity] = await self.repository.patch(id=id, patches=patches)

		logger.info(msg="End")

		return result

	# endregion
