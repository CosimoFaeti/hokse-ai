from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS

def model() -> BaseChatModel:
    """"""
    logger.debug(msg=f"Building LLM for providers={SETTINGS.LLM_PROVIDER}")

    if SETTINGS.LLM_PROVIDER == "ollama":
        base_url = (
            f"http://{SETTINGS.LLM_HOST}:{SETTINGS.LLM_PORT}"
            if SETTINGS.LLM_HOST and SETTINGS.LLM_PORT
            else "http://localhost:11434"
        )
        return ChatOllama(
            model=SETTINGS.LLM_MODEL,
            base_url=base_url,
            temperature=0.0,
        )
    elif SETTINGS.LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=SETTINGS.LLM_MODEL,
            google_api_key=SETTINGS.LLM_API_KEY,
            temperature=0.0
        )