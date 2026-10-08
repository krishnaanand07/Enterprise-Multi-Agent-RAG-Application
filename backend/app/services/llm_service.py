import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings


class LLMService:
    """
    Centralized LLM Service for Google Gemini API.
    All Gemini interactions in the app resolve through this single service.
    """
    def __init__(self):
        api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            os.environ["GEMINI_API_KEY"] = api_key

    def get_llm(self, temperature: float = 0.2) -> BaseChatModel:
        """Returns ChatGoogleGenerativeAI instance using configured Gemini model."""
        api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Please set GEMINI_API_KEY in environment or .env file.")

        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True
        )


llm_service = LLMService()

