from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from container import Container
from dependencies import get_sql_template_service, get_nosql_template_service, get_graph_template_service, \
	get_vector_template_service
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.infrastructure.clients.agent_client import AgentClient
from src.infrastructure.clients.strava_client import StravaClient
from src.persistence.managers.sql_database_manager import SQLDatabaseManager
from src.presentation.endpoints.health.health_endpoints import health_router
from src.presentation.endpoints.authentication.auth_endpoints import auth_router
from src.presentation.endpoints.chats.chats_endpoints import chats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Define startup and cleanup operations for a FastAPI app.

	:param FastAPI app: FastAPI app to
	"""

	# Initialize SQL database connection and create tables
	logger.info(msg="Initializing SQL database connection.")
	await SQLDatabaseManager().create_tables()
	logger.info(msg="SQL database connection correctly initialized.")

	# Initialize Strava connection
	logger.info(msg="Initializing Strava connection.")
	StravaClient()
	logger.info(msg="Strava connection correctly initialized.")

	# Initialize Agent
	logger.info(msg="Initializing Agent.")
	AgentClient()
	logger.info(msg="Agent correctly initialized.")

	logger.info(msg="App is now ready to manage requests.")

	yield

container = Container()

app = FastAPI(
	title="Hokse-ai",
	summary="This is hokse-ai.",
	description="The swagger offers the possibility to perform simple CRUD operations.",
	docs_url="/docs",
	version="1.0",
	lifespan=lifespan,
)
# Include endpoints routers
app.include_router(router=health_router)
app.include_router(router=auth_router)
app.include_router(router=chats_router)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


logger.info(msg=f"Starting server on 0.0.0.0:{SETTINGS.PORT}")

uvicorn.run(app=app, host="0.0.0.0", port=SETTINGS.PORT, log_level="error")
