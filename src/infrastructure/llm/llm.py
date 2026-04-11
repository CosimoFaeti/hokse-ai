from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from src.domain.utilities.logger import logger
from src.domain.utilities.settings import SETTINGS

def model() -> BaseChatModel:
    """"""
    logger.debug(msg=f"Building LLM for providers={SETTINGS.LLM_PROVIDER}")

    if SETTINGS.LLM_PROVIDER == "ollama":
        return ChatOllama(
            model=SETTINGS.LLM_MODEL,
            temperature=0.0,
        )
    elif SETTINGS.LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=SETTINGS.LLM_MODEL,
            google_api_key=SETTINGS.LLM_API_KEY,
            temperature=0.0
        )