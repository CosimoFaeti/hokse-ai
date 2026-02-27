from abc import ABC, abstractmethod
from pydantic import UUID4

from src.domain.entities.patch_entity import PatchEntity
from src.domain.entities.template_entity import TemplateEntity
from src.domain.results.result import Result


class IGraphTemplateRepository(ABC):

    @staticmethod
    @abstractmethod
    async def post(entity: TemplateEntity) -> Result[TemplateEntity]:
        """
		Create a new template.

		:param TemplateEntity entity:
		:return: a Result containing the created entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

        pass

    # endregion

    # region GET

    @staticmethod
    @abstractmethod
    async def get(id: UUID4) -> Result[TemplateEntity]:
        """
		Retrieve the template with the given id.

		:param UUID4 id: id of the Template to retrieve.
		:return: a Result containing the retrieved entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

        pass

    # endregion

    # region PUT

    @staticmethod
    @abstractmethod
    async def put(id: UUID4, entity: TemplateEntity) -> Result[TemplateEntity]:
        """
		Replace the template with the given id with the one passed as parameter.

		:param UUID4 id: id of the Template to update.
		:param TemplateEntity entity: Template used for overwriting the old template value.
		:return: a Result containing the updated entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

        pass

    # endregion

    # region DELETE
    @staticmethod
    @abstractmethod
    async def delete(id: UUID4) -> Result[TemplateEntity]:
        """
		Delete a template.

		:param UUID4 id: id of the Template to delete.
		:return: a Result containing the deleted entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

        pass

    # endregion

    # region PATCH
    @staticmethod
    @abstractmethod
    async def patch(id: UUID4, patches: list[PatchEntity]):
        """
		Update the template with the given id with the given patches.

		:param UUID4 id: id of the Template to patch.
		:param list[PatchEntity] patches: list of patches to apply to the template.
		:return: a Result containing the patched entity if the operation has been successful, a Result containing the
		error if the operation failed.
		:rtype: Result[TemplateEntity]
		"""

        pass