from pydantic import UUID4
from sqlmodel import select

from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.objects.template import Template
from src.persistence.managers.sql_database_manager import SQLDatabaseManager
import jsonpatch


class SQLTemplateRepository:
	# region POST
	@exception_handler
	@staticmethod
	async def post(entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Create a new Template.


		:param TemplateEntity entity: entity containing the information about the Template to be created.
		:return: a Result object containing the created Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		# TODO check if this mapping can be avoided, or add a mapper instead
		template: Template = Template(**entity.model_dump())

		async with SQLDatabaseManager().get_session() as session:
			session.add(instance=template)
			await session.commit()
			await session.refresh(template)

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region GET
	@exception_handler
	@staticmethod
	async def get(id: UUID4) -> Result[TemplateEntity]:
		"""
		Retrieve the Template with the given id.

		:param UUID4 id: id of the Template to be retrieved.
		:return: a Result object containing the retrieved Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}")

		statement = select(Template).where(Template.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement=statement)

			template = results.first()

			if template is None:
				logger.error(msg=f"No template with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

			entity = Template(**template.model_dump())

			"""
            TODO alternative, to be tested
            template = session.get(Template, id)
            """

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region DELETE
	@exception_handler
	@staticmethod
	async def delete(id: UUID4) -> Result[TemplateEntity]:
		"""
		Delete the Template with the given id.

		:param UUID4 id: id of the Template to be deleted.
		:return: a Result object containing the deleted Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}")

		statement = select(Template).where(Template.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement)

			template = results.first()

			if template is None:
				logger.error(msg=f"No template with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

			await session.delete(template)
			await session.commit()

			entity = Template(**template.model_dump())

			"""
            TODO alternative, to be tested
            template = session.get(Template, id)
            """

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region UPDATE
	@exception_handler
	@staticmethod
	async def put(id: UUID4, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""
		Replace the Template with the given id with the one passed as parameter.

		:param UUID4 id: id of the Template to be replaced.
		:param TemplateEntity entity: entity containing the new Template information.
		:return: a Result object containing the updated Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}, entity={entity}")

		statement = select(Template).where(Template.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement)
			template = results.first()

			if template is None:
				logger.error(msg=f"No template with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

			# TODO is there a way to do it dynamically?
			template.description = entity.description
			session.add(template)
			await session.commit()
			await session.refresh(template)

			entity = Template(**template.model_dump())

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# TODO here should i send directly the patched entity?
	# region PATCH
	@exception_handler
	@staticmethod
	async def patch(id: UUID4, patches: list[PatchEntity]) -> Result[TemplateEntity]:
		"""
		Patch the Template with the given id with the list of patches passed as parameter.

		:param UUID4 id: id of the Template to be replaced.
		:param list[PatchEntity] patches: list containing patches information.
		:return: a Result object containing the patched Template if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[TemplateEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}, patches={patches}")

		async with SQLDatabaseManager().get_session() as session:
			statement = select(Template).where(Template.id == id)
			results = await session.exec(statement)
			template = results.first()

			if template is None:
				logger.error(msg=f"No template with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="template", key=id))

			patched_template_dict = jsonpatch.apply_patch(
				template.model_dump(), [patch.model_dump() for patch in patches]
			)

			patched_template = Template(**patched_template_dict)

			await session.delete(template)  # TODO: da cambiare
			session.add(patched_template)
			await session.commit()
			await session.refresh(patched_template)

			entity: TemplateEntity = TemplateEntity(**patched_template_dict)

		logger.info(msg="End")

		return Result.ok(value=entity)


# endregion
