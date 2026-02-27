from fastapi import APIRouter

from src.domain.utilities.logger import logger

health_router = APIRouter(prefix="", tags=["Health"])


# region POST
@health_router.post(
	path="/healthz",
	summary="Determine if the service is up and running.",
	description="Determine if the service is up and running.",
	status_code=204,
	include_in_schema=False,  # exclude from swagger
)
async def healthz() -> None:
	"""
	Healthcheck endpoint to verify if the microservice is ready to manage requests.
	"""

	logger.info(msg="Calling GET /healthz")

	logger.info(msg="Successful returning GET /healthz")
