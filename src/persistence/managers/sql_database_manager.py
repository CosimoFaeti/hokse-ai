from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.domain.utilities.singleton import Singleton
from sqlalchemy import URL


class SQLDatabaseManager(metaclass=Singleton):
	"""
	Utility class to manage SQL database connection.

	:param AsyncEngine engine: asynchronous SQL database engine.
	"""

	def __init__(self):
		"""
		Initialize SQL database connection using info from environment variables.
		"""

		logger.info(msg="Start")

		url: URL = URL.create(
			drivername=SETTINGS.RELATIONAL_DB_TYPE,
			username=SETTINGS.RELATIONAL_DB_USER,
			password=SETTINGS.RELATIONAL_DB_PASSWORD.get_secret_value(),  # plain (unescaped) text
			host=SETTINGS.RELATIONAL_DB_HOST,
			port=SETTINGS.RELATIONAL_DB_PORT,
			database=SETTINGS.RELATIONAL_DB_NAME,
		)

		logger.info(msg=f"Connecting to SQL database with url={url}")

		self.engine: AsyncEngine = create_async_engine(url=url, pool_size=20)

		logger.info(msg="End")

	async def create_tables(self) -> None:
		"""
		Create tables on the SQL database. In order to create tables, objects that extends SQLmodel must be imported
		before using this function.
		"""

		logger.info(msg="Start")

		async with self.engine.begin() as connection:
			await connection.run_sync(SQLModel.metadata.create_all)

		logger.info(msg="End")

	def get_session_old(self) -> AsyncSession:
		"""
		Retrieve an asynchronous session for the SQL database.

		:return: an SQL database asynchronous session.
		:rtype: AsyncSession
		"""

		logger.info(msg="Start")

		async_session = AsyncSession(self.engine)

		logger.info(msg="End")

		return async_session

	@asynccontextmanager
	async def get_session(self) -> AsyncSession:
		"""
		Retrieve an asynchronous session for the SQL database.

		:return: an SQL database asynchronous session.
		:rtype: AsyncSession
		"""
		logger.info(msg="Start")
		async_session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
		async with async_session() as session:
			logger.info(msg="End")
			yield session


"""

        
# Function to create a new user in the database
async def create_user(user: User) -> User:
    async with get_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
"""
