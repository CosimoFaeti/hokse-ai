import secrets

from fastapi import APIRouter, Depends, Body, HTTPException, Path
from fastapi.responses import RedirectResponse
from pydantic import PositiveInt

from dependencies import get_auth_service
from src.domain.entities.strava_token_entity import StravaTokenEntity
from src.domain.results.result import Result
from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS
from src.application.interfaces.i_auth_service import IAuthService
from src.presentation.DTOs.auth.callback.get_callback_input_dto import GetCallbackInputDTO
from src.presentation.DTOs.auth.status.get_status_input_dto import GetStatusInputDTO
from src.presentation.DTOs.auth.status.get_status_output_dto import GetStatusOutputDTO
from src.presentation.DTOs.auth.revoke.delete_revoke_output_dto import DeleteRevokeOutputDTO
from src.presentation.examples.auth.get_strava_response_examples import GET_STRAVA_RESPONSE_EXAMPLES
from src.presentation.examples.auth.get_callback_response_examples import GET_CALLBACK_RESPONSE_EXAMPLES
from src.presentation.examples.auth.get_status_response_examples import GET_STATUS_RESPONSE_EXAMPLES
from src.presentation.examples.auth.delete_revoke_response_examples import DELETE_REVOKE_RESPONSE_EXAMPLES
from src.presentation.examples.auth.delete_revoke_request_examples import DELETE_REVOKE_PATH_EXAMPLE
from src.presentation.mappers.auth.get_status_mappers import GetStatusMappers
from src.presentation.mappers.auth.delete_revoke_mappers import DeleteRevokeMappers

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

_state_store: set[str] = set()

# region GET
@auth_router.get(
    path="/strava",
    summary="Initiate Strava Oauth flow.",
    description="Redirect to Strava consent screen",
    status_code=201,
    responses=GET_STRAVA_RESPONSE_EXAMPLES,
)
async def strava_login() -> RedirectResponse:
    """"""
    logger.info(msg="Calling GET /auth/strava")

    state = secrets.token_urlsafe(16)
    _state_store.add(state)
    logger.debug(msg=f"OAuth login initiated — state={state}")

    params = (
        f"client_id={SETTINGS.STRAVA_CLIENT_ID}",
        f"&redirect_uri={SETTINGS.STRAVA_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SETTINGS.STRAVA_SCOPE}"
        f"&state={state}"
    )

    logger.info(msg="Successfully returning from GET /auth/strava")

    return RedirectResponse(
        url=f"{SETTINGS.STRAVA_OAUTH_URL}?{params}",
    )

@auth_router.get(
    path="/callback",
    summary="Strava Oauth callback.",
    description="OAuth callback, exchange code, redirect to Streamlit",
    status_code=201,
    responses=GET_CALLBACK_RESPONSE_EXAMPLES,
)
async def strava_callback(
        state: str,
        dto: GetCallbackInputDTO = Body(examples=GET_CALLBACK_RESPONSE_EXAMPLES),
        auth_service: IAuthService = Depends(get_auth_service),
) -> RedirectResponse:
    """"""
    logger.info(msg="Calling GET /auth/callback")

    if state not in _state_store:
        logger.warning(msg=f"Invalid OAuth state: {state}")
        raise HTTPException(status_code=400, detail="Invalid OAuth state parameter.")
    _state_store.discard(state)

    result: Result[StravaTokenEntity] = await auth_service.exchange_code(code=dto.code)

    if result.failed:
        raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

    token: StravaTokenEntity = result.value

    streamlit_url = SETTINGS.api_base_url.replace("8000", "8501")

    logger.info(msg="Successfully returning from GET /auth/callback")

    return RedirectResponse(url=f"{streamlit_url}?athlete_id={token.athlete_id}&connected=true")

@auth_router.get(
    path="/status",
    summary="Check Strava connection status.",
    description="Check connection status for an athlete.",
    status_code=201,
    responses=GET_STATUS_RESPONSE_EXAMPLES,
)
async def auth_status(
        dto: GetStatusInputDTO = Body(examples=GET_STATUS_RESPONSE_EXAMPLES),
        auth_service: IAuthService = Depends(get_auth_service),
) -> GetStatusOutputDTO:
    """"""
    logger.info(msg="Calling GET /auth/status")

    result: Result[StravaTokenEntity] = await auth_service.get_valid_token(athlete_id=dto.athlete_id)

    if result.failed:
        raise HTTPException(detail=result.error.message, status_code=result.error.status_code)

    output: GetStatusOutputDTO = GetStatusMappers().to_dto(entity=result.value)

    logger.info(msg="Successfully returning from GET /auth/status")

    return output
# endregion

# region DELETE
@auth_router.delete(
    path="/{athlete_id}",
    summary="Disconnect Strava account.",
    description="Disconnect (revoke stored token)",
    responses=DELETE_REVOKE_RESPONSE_EXAMPLES,
)
async def revoke(
        athlete_id: int = Path(example=DELETE_REVOKE_PATH_EXAMPLE),
        auth_service: IAuthService = Depends(get_auth_service),
) -> DeleteRevokeOutputDTO:
    """"""
    logger.info(msg="Calling DELETE /auth/{athlete_id}")

    result: Result[StravaTokenEntity] = await auth_service.revoke(athlete_id=athlete_id)

    if result.failed:
        raise HTTPException(status_code=500, detail=f"Failed to revoke: {result.error}")

    output: DeleteRevokeOutputDTO = DeleteRevokeMappers.to_dto(entity=result.value)

    logger.info(msg="Successfully returning from DELETE /auth/{athlete_id}")

    return output

