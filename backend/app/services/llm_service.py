import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings


class LLMService:
    """
    Abstracted LLM Service for Google Gemini API.
    All Gemini interactions in the app go through this service.
    """
    def __init__(self):
        api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key

        self.model_name = settings.GEMINI_MODEL

    def get_llm(self, temperature: float = 0.2) -> BaseChatModel:
        """Returns ChatGoogleGenerativeAI instance."""
        api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True
        )


llm_service = LLMService()
