from abc import abstractmethod, ABC

from pydantic import UUID4

from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.results.result import Result



class INOSQLTemplateRepository(ABC):
	# region POST
	@staticmethod
	@abstractmethod
	async def post(entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Create a new Template.


		:param TemplateEntity entity: entity containing the information about the Template to be created.
		:return: a Result object containing the created Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		pass

	# endregion

	# region GET
	@staticmethod
	@abstractmethod
	async def get(id: UUID4) -> Result[TemplateEntity]:
		"""
		Retrieve the Template with the given id.

		:param UUID4 id: id of the Template to be retrieved.
		:return: a Result object containing the retrieved Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		pass

	# endregion

	# region DELETE
	@staticmethod
	@abstractmethod
	async def delete(id: UUID4) -> Result[TemplateEntity]:
		"""
		Delete the Template with the given id.

		:param UUID4 id: id of the Template to be deleted.
		:return: a Result object containing the deleted Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		pass

	# endregion

	# region UPDATE
	@staticmethod
	@abstractmethod
	async def put(id: UUID4, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Replace the Template with the given id with the one passed as parameter.

		:param UUID4 id: id of the Template to be replaced.
		:param TemplateEntity entity: entity containing the new Template information.
		:return: a Result object containing the updated Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		pass

	# endregion

	# TODO here should i send directly the patched entity?
	# region PATCH
	@staticmethod
	@abstractmethod
	async def patch(id: UUID4, patches: list[PatchEntity]) -> Result[TemplateEntity]:
		"""
		Patch the Template with the given id with the list of patches passed as parameter.

		:param UUID4 id: id of the Template to be replaced.
		:param list[PatchEntity] patches: list containing patches information.
		:return: a Result object containing the patched Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		pass

# endregion
