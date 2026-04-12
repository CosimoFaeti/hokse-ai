import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.dependencies import get_agent_client
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.persistence.managers.nosql_database_manager import NoSQLDatabaseManager
from src.presentation.endpoints.health.health_endpoints import health_router
from src.presentation.endpoints.authentication.auth_endpoints import auth_router
from src.presentation.endpoints.agent.agent_endpoints import agent_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Define startup and cleanup operations for Hokse-ai app.

	:param FastAPI app: FastAPI app to
	"""

	# Initialize NoSQL database connection and create tables
	logger.info(msg="Initializing NoSQL database connection.")
	await NoSQLDatabaseManager().create_collections()
	logger.info(msg="NoSQL database connection correctly initialized.")

	# Initialize Agent
	logger.info(msg="Initializing LangGraph agent.")
	get_agent_client()
	logger.info(msg="Agent correctly initialized.")

	logger.info(msg="App is now ready to manage requests.")
	yield

app = FastAPI(
	title="Hokse-ai",
	summary="An AI-powered personal training coach that analyses your Strava data.",
	description="The swagger offers the possibility to perform simple CRUD operations.",
	docs_url="/docs",
	version="0.1.0",
	lifespan=lifespan,
)
# Include endpoints routers
app.include_router(router=health_router)
app.include_router(router=auth_router)
app.include_router(router=agent_router)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


if __name__ == "__main__":
    logger.info(msg=f"Starting server on 0.0.0.0:{SETTINGS.API_PORT}")
    uvicorn.run(app=app, host="0.0.0.0", port=SETTINGS.API_PORT, log_level="error")
