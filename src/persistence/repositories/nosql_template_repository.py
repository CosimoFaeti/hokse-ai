from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.objects.nosql_template import NoSQLTemplate
from pydantic import UUID4
import jsonpatch
from beanie.exceptions import DocumentNotFound


class NoSQLTemplateRepository:
	"""Repository to perform operations on ``templates`` NoSQL collection."""

	# region POST

	@exception_handler
	@staticmethod
	async def post(entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Create a new template.

		:param TemplateEntity entity:
		:return: a Result containing the created entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		nosql_template: NoSQLTemplate = NoSQLTemplate(**entity.model_dump())

		await nosql_template.insert()

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region GET

	@exception_handler
	@staticmethod
	async def get(id: UUID4) -> Result[TemplateEntity]:
		"""
		Retrieve the template with the given id.

		:param UUID4 id: id of the Template to retrieve.
		:return: a Result containing the retrieved entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result = await NoSQLTemplate.get(document_id=id)

		if result is None:
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

		logger.info(msg="End")

		template: TemplateEntity = TemplateEntity(**result.model_dump())

		return Result.ok(value=template)

	# endregion

	# region PUT

	@exception_handler
	@staticmethod
	async def put(id: UUID4, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Replace the template with the given id with the one passed as parameter.

		:param UUID4 id: id of the Template to update.
		:param TemplateEntity entity: Template used for overwriting the old template value.
		:return: a Result containing the updated entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		template: NoSQLTemplate = NoSQLTemplate(**entity.model_dump())
		template.id = id
		try:
			await template.replace()
		except (ValueError, DocumentNotFound):
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(key=str(id), type="template"))

		result: TemplateEntity = TemplateEntity(**template.model_dump())

		logger.info(msg="End")

		return Result.ok(value=result)

	# endregion

	# region DELETE
	@exception_handler
	@staticmethod
	async def delete(id: UUID4) -> Result[TemplateEntity]:
		"""
		Delete a template.

		:param UUID4 id: id of the Template to delete.
		:return: a Result containing the deleted entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")

		result = await NoSQLTemplate.get(document_id=id)

		if result is None:
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

		await result.delete()

		template: TemplateEntity = TemplateEntity(**result.model_dump())

		logger.info(msg="End")

		return Result.ok(value=template)

	# endregion

	# region PATCH
	@exception_handler
	@staticmethod
	async def patch(id: UUID4, patches: list[PatchEntity]):
		"""
		Update the template with the given id with the given patches.

		:param UUID4 id: id of the Template to patch.
		:param list[PatchEntity] patches: list of patches to apply to the template.
		:return: a Result containing the patched entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}, patches={patches}")

		result = await NoSQLTemplate.get(document_id=id)

		if result is None:
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

		patched_template_dict: dict = jsonpatch.apply_patch(
			doc=result.model_dump(), patch=[patch.model_dump() for patch in patches]
		)

		patched_template: NoSQLTemplate = NoSQLTemplate(**patched_template_dict)
		patched_template.id = id

		try:
			await patched_template.replace()
		except (ValueError, DocumentNotFound):
			logger.error(msg=f"Entry of type template with key={id} does not exist.")
			return Result.fail(error=GenericErrors.not_found_error(key=str(id), type="template"))

		logger.info(msg="End")

		return Result.ok(value=patched_template)

	# endregion
