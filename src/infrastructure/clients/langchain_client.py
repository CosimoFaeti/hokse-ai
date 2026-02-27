import uuid
from datetime import datetime

from src.domain.entities.vector_database_template_entity import VectorDatabaseTemplateEntity
from src.domain.entities.vector_database_template_payload_entity import VectorDatabaseTemplatePayloadEntity
from src.domain.results.result import Result
from src.domain.utilities.constants import date_format
from src.domain.utilities.exception_handler import exception_handler
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


class LangchainClient(metaclass=Singleton):
	"""Utility class to manage connections to AI models using Langchain."""

	def __init__(self):
		"""
		Create a client to communicate with an embedder model.
		"""

		logger.info(msg="Start")

		logger.info(
			msg=f"Initializing connection to embedder with base_url={SETTINGS.EMBEDDER_HOST}:{SETTINGS.EMBEDDER_PORT} and model={SETTINGS.EMBEDDER_NAME}"
		)
		self.embedder = OllamaEmbeddings(
			base_url=f"{SETTINGS.EMBEDDER_HOST}:{SETTINGS.EMBEDDER_PORT}", model=SETTINGS.EMBEDDER_NAME
		)

		logger.info(msg="End")

	@exception_handler
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

		logger.info(msg="Start")
		logger.debug(
			msg=f"Input params: text=text of {len(text)} chars, chunk_size={chunk_size}, chunk_overlap={chunk_overlap}"
		)

		text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

		chunks: list[str] = text_splitter.split_text(text=text)

		logger.info(msg=f"Given text has been split into {len(chunks)} chunks.")

		result: [VectorDatabaseTemplateEntity] = []

		for index, chunk in enumerate(chunks):
			logger.debug(msg=f"Creating the embeddings for chunk {index} with text {text}")

			vector: list[float] = await self.embedder.aembed_query(text=chunk)

			result.append(
				VectorDatabaseTemplateEntity(
					id=str(uuid.uuid4()),
					vector=vector,
					payload=VectorDatabaseTemplatePayloadEntity(
						text=chunk, upload_date=datetime.now().strftime(format=date_format)
					),
				)
			)

		logger.info(msg="End")
		logger.debug(msg=f"Return value=list of {len(result)} points.")

		return Result.ok(value=result)
