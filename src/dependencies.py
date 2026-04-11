from functools import lru_cache

from src.application.interfaces.i_auth_service import IAuthService
from src.application.interfaces.i_activity_service import IActivityService
from src.application.interfaces.i_agent_service import IAgentService
from src.application.services.auth_service import AuthService
from src.application.services.agent_service import AgentService
from src.application.services.activity_service import ActivityService
from src.infrastructure.clients.agent_client import AgentClient
from src.infrastructure.clients.strava_client import StravaClient
from src.persistence.repositories.activity_repository import ActivityRepository
from src.persistence.repositories.strava_token_repository import StravaTokenRepository

# -- Repositories --
@lru_cache
def get_strava_token_repository() -> StravaTokenRepository:
    return StravaTokenRepository()

@lru_cache
def get_activity_repository() -> ActivityRepository:
    return ActivityRepository()

# -- Infra clients --
def get_agent_client() -> AgentClient:
    return AgentClient()

def get_strava_client() -> StravaClient:
    return StravaClient(strava_token_repository=get_strava_token_repository())

# -- Services --
def get_auth_service() -> IAuthService:
    return AuthService(
        strava_token_repository=get_strava_token_repository(),
        strava_client=get_strava_client(),
    )

def get_activity_service() -> IActivityService:
    return ActivityService(
        activity_repository=get_activity_repository(),
        strava_client=get_strava_client(),
        auth_service=get_auth_service(),
    )

def get_agent_service() -> IAgentService:
    return AgentService(
        activity_service=get_activity_service(),
        agent_client=get_agent_client(),
    )