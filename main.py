from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from container import Container
from dependencies import get_sql_template_service, get_nosql_template_service, get_graph_template_service, \
	get_vector_template_service
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.infrastructure.clients.langchain_client import LangchainClient
from src.infrastructure.clients.redis_client import RedisClient
from src.persistence.managers.graph_database_manager import GraphDatabaseManager
from src.persistence.managers.nosql_database_manager import NoSQLDatabaseManager
from src.persistence.managers.sql_database_manager import SQLDatabaseManager
from src.persistence.managers.vector_db_database_manager import VectorDBDatabaseManager
from src.presentation.endpoints.health.health_endpoints import health_router
from src.presentation.endpoints.templates.graph_template_endpoints import graph_template_router
from src.presentation.endpoints.templates.sql_template_endpoints import sql_template_router
from src.presentation.endpoints.templates.nosql_template_endpoints import nosql_template_router
from src.presentation.endpoints.templates.vector_template_endpoints import vector_template_router

# TODO it is incorrect to directly call persistence (?)
@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Define startup and cleanup operations for a FastAPI app.

	:param FastAPI app: FastAPI app to
	"""

	# TODO evaluate if moving these lines into the init of persistence or infrastructure and simply import them here

	# Initialize SQL database connection and create tables
	logger.info(msg="Initializing SQL database connection.")
	await SQLDatabaseManager().create_tables()
	logger.info(msg="SQL database connection correctly initialized.")

	# Initialize NoSQL database connection and create tables
	logger.info(msg="Initializing NoSQL database connection.")
	await NoSQLDatabaseManager().create_collections()
	logger.info(msg="NoSQL database connection correctly initialized.")

	# Initialize Vector database connection
	logger.info(msg="Initializing Vector database connection.")
	VectorDBDatabaseManager().health_check()
	await VectorDBDatabaseManager().create_collection(collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME)
	logger.info(msg="Vector database connection correctly initialized.")

	# Initialize Graph database connection
	logger.info(msg="Initializing Graph database connection.")
	GraphDatabaseManager()
	logger.info(msg="Graph database connection correctly initialized.")

	# Initialize Redis connection
	logger.info(msg="Initializing Redis connection.")
	RedisClient()
	logger.info(msg="Redisconnection correctly initialized.")

	# Initialize Langchain agent
	logger.info(msg="Initializing Langchain agent.")
	LangchainClient()
	logger.info(msg="Langchain agent correctly initialized.")

	logger.info(msg="App is now ready to manage requests.")

	yield

container = Container()

app = FastAPI(
	title="Python API Template",
	summary="This is a template backend written in Python.",
	description="The swagger offers the possibility to perform simple CRUD operations.",
	docs_url="/docs",
	version="1.0",
	lifespan=lifespan,
)

# override dependencies
app.dependency_overrides[get_sql_template_service] = lambda: container.sql_template_service()
app.dependency_overrides[get_nosql_template_service] = lambda: container.nosql_template_repository()
app.dependency_overrides[get_graph_template_service] = lambda: container.graph_template_service()
app.dependency_overrides[get_vector_template_service] = lambda: container.vector_template_service()

# Include endpoints routers
app.include_router(router=health_router)
app.include_router(router=sql_template_router)
app.include_router(router=nosql_template_router)
app.include_router(router=vector_template_router)
app.include_router(router=graph_template_router)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


logger.info(msg=f"Starting server on 0.0.0.0:{SETTINGS.PORT}")

uvicorn.run(app=app, host="0.0.0.0", port=SETTINGS.PORT, log_level="error")
