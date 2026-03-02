import jsonpatch

from pydantic import UUID4
from sqlmodel import select

from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.entities.patch_entity import PatchEntity
from src.domain.errors.generic_errors import GenericErrors
from src.domain.results.result import Result
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.persistence.objects.sql_strava_token import StravaToken
from src.persistence.managers.sql_database_manager import SQLDatabaseManager



class StravaTokenRepository:
	"""utility class to perform CRUD operations on Strava Tokens"""

	# region POST
	@exception_handler
	@staticmethod
	async def post(entity: StravaTokenEntity) -> Result[StravaTokenEntity]:
		"""
		Create a new Strava token.


		:param StravaTokenEntity entity: entity containing the information about the Strava token to be created.
		:return: a Result object containing the created Strava token if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[StravaTokenEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: entity={entity}")

		# TODO check if this mapping can be avoided, or add a mapper instead
		strava_token: StravaToken = StravaToken(**entity.model_dump())

		async with SQLDatabaseManager().get_session() as session:
			session.add(instance=strava_token)
			await session.commit()
			await session.refresh(strava_token)

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# region GET
	@exception_handler
	@staticmethod
	async def get(id: UUID4) -> Result[StravaTokenEntity]:
		"""
		Retrieve the Strava token with the given id.

		:param UUID4 id: id of the Strava token to be retrieved.
		:return: a Result object containing the retrieved Strava token if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[StravaTokenEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}")

		statement = select(StravaToken).where(StravaToken.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement=statement)

			strava_token = results.first()

			if strava_token is None:
				logger.error(msg=f"No strava_token with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

			entity = StravaToken(**strava_token.model_dump())

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
	async def delete(id: UUID4) -> Result[StravaTokenEntity]:
		"""
		Delete the Strava token with the given id.

		:param UUID4 id: id of the Strava token to be deleted.
		:return: a Result object containing the deleted Strava token if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[StravaTokenEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}")

		statement = select(StravaToken).where(StravaToken.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement)

			strava_token = results.first()

			if strava_token is None:
				logger.error(msg=f"No strava_token with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

			await session.delete(strava_token)
			await session.commit()

			entity = StravaToken(**strava_token.model_dump())

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
	async def put(id: UUID4, entity: StravaTokenEntity) -> Result[StravaTokenEntity]:
		"""
		Replace the Strava token with the given id with the one passed as parameter.

		:param UUID4 id: id of the Template to be replaced.
		:param StravaTokenEntity entity: entity containing the new Strava token information.
		:return: a Result object containing the updated Strava token if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[StravaTokenEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}, entity={entity}")

		statement = select(StravaToken).where(StravaToken.id == id)

		async with SQLDatabaseManager().get_session() as session:
			results = await session.exec(statement)
			strava_token = results.first()

			if strava_token is None:
				logger.error(msg=f"No strava_token with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

			# TODO is there a way to do it dynamically?
			strava_token.access_token = entity.access_token
			strava_token.refresh_token = entity.refresh_token
			strava_token.expires_at = entity.expires_at
			session.add(strava_token)
			await session.commit()
			await session.refresh(strava_token)

			entity = StravaToken(**strava_token.model_dump())

		logger.info(msg="End")

		return Result.ok(value=entity)

	# endregion

	# TODO here should i send directly the patched entity?
	# region PATCH
	@exception_handler
	@staticmethod
	async def patch(id: UUID4, patches: list[PatchEntity]) -> Result[StravaTokenEntity]:
		"""
		Patch the Strava token with the given id with the list of patches passed as parameter.

		:param UUID4 id: id of the Strava token to be replaced.
		:param list[PatchEntity] patches: list containing patches information.
		:return: a Result object containing the patched Strava token if function has been successful, a Result object containing
		the error otherwise.
		:rtype: Result[StravaTokenEntity]
		"""

		logger.info(msg="Start")
		logger.debug(msg=f"Input params: id={id}, patches={patches}")

		async with SQLDatabaseManager().get_session() as session:
			statement = select(StravaToken).where(StravaToken.id == id)
			results = await session.exec(statement)
			strava_token = results.first()

			if strava_token is None:
				logger.error(msg=f"No strava_token with id={id} found")
				return Result.fail(error=GenericErrors.not_found_error(type="strava_token", key=id))

			patched_strava_token_dict = jsonpatch.apply_patch(
				strava_token.model_dump(), [patch.model_dump() for patch in patches]
			)

			patched_strava_token = StravaToken(**patched_strava_token_dict)

			await session.delete(strava_token)  # TODO: da cambiare
			session.add(patched_strava_token)
			await session.commit()
			await session.refresh(patched_strava_token)

			entity: StravaTokenEntity = StravaTokenEntity(**patched_strava_token_dict)

		logger.info(msg="End")

		return Result.ok(value=entity)


# endregion
