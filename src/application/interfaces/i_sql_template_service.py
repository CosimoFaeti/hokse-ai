from abc import abstractmethod, ABC

from src.domain.entities.template_entity import TemplateEntity
from src.domain.results.result import Result


class ISQLTemplateService(ABC):
	@abstractmethod
	async def post(self, entity: TemplateEntity) -> Result[TemplateEntity]:
		"""

		:param entity:
		:return:
		"""

		pass
