from fastapi import Security, HTTPException, status, Request
from fastapi.routing import APIRoute

from src.domain.utilities.logger import logger
from src.presentation.utils.authentication_type import AuthenticationType

# Mock functions to validate different authentication types
def validate_jwt(token: str) -> bool:
    return token == "valid-jwt-token"  # Replace with actual JWT validation logic

def validate_api_key(api_key: str) -> bool:
    return api_key == "valid-api-key"  # Replace with actual API key validation logic


async def authorize(request: Request) -> None:
    """
    Authenticate an incoming request according to the security level of the route.

    :param Request request: the incoming request
    :raises: HTTPException if the request is not authenticated or the authentication type is not recognized.
    """

    logger.info(msg="Start")

    route = request.scope.get("route", {})

    if isinstance(route, APIRoute):
        openapi_extra = route.openapi_extra or {}

        # Assuming the default authentication type is PUBLIC
        authentication_type = openapi_extra.get("authentication_type", AuthenticationType.PUBLIC)

        logger.debug(msg=f"Authentication type for route {route.path} is {authentication_type.value}")

        match authentication_type:
            case AuthenticationType.TOKEN:
                token = request.headers.get("Authorization", "")
                if not token:
                    logger.error(msg=f"No token provided for request to route {route.path}.")
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No token provided for request to route {route.path}.")
                if not validate_jwt(token):
                    logger.error(msg=f"Provided token for request to route {route.path} is not valid.")
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Provided token for request to route {route.path} is not valid.")
            case AuthenticationType.API_KEY:
                api_key = request.headers.get("X-API-Key")
                if not api_key:
                    logger.error(
                        msg=f"No API KEY provided for request to route {route.path}.")
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No API KEY provided for request to route {route.path}.")
                if not validate_api_key(api_key):
                    logger.error(msg=f"Provided API KEY for route {route.path} is not valid.")
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Provided API KEY for route {route.path} is not valid.")
            case AuthenticationType.PUBLIC:
                pass
            case _:
                logger.error(msg=f"Authentication type {authentication_type} for route {route.path} is not supported")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication type {authentication_type} for route {route.path} is not supported")

        logger.info(msg="End")