from abc import ABC, abstractmethod

from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.results.result import Result


class ILangchainClient(ABC):

	@abstractmethod
	async def embed(
			self, text: str, chunk_size: int = 1024, chunk_overlap: int = 128
	) -> Result[list[VectorDatabaseTemplateEntity]]:
		"""
		Creates the embedding for the given text.

		:param str text: text for which embeddings must be created.
		:param int chunk_size: size used to split text in chunks.
		:param int chunk_overlap: overlap between two consecutive chunks.
		:return: a Result object containing the list of chunks and their vectors if the operation has been successful,
		a Result containing the error if the operation failed.
		:rtype: Result[list[VectorDatabaseTemplateEntity]
		"""

		pass
