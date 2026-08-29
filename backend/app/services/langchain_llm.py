"""
LangChain-compatible LLM wrappers.

These wrappers allow our Gemini/OpenAI models to be used
with LangChain chains, agents, and LangGraph nodes.

Usage:
    from app.services.langchain_llm import get_llm
    llm = get_llm()
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.config.settings import settings


def get_llm(
    provider: str = None,
    temperature: float = 0.7,
    streaming: bool = False,
):
    """
    Get a LangChain-compatible LLM instance.

    Args:
        provider: "gemini" or "openai". Defaults to settings.LLM_PROVIDER.
        temperature: Model creativity (0.0 - 1.0).
        streaming: Enable streaming responses.

    Returns:
        A LangChain ChatModel instance.
    """
    provider = provider or settings.LLM_PROVIDER

    if provider == "gemini":
        api_key = settings.GOOGLE_API_KEY.strip() if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.strip() else "NO_API_KEY_PROVIDED"
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=api_key,
            temperature=temperature,
            streaming=streaming,
            convert_system_message_to_human=True,
        )
    elif provider == "openai":
        api_key = settings.OPENAI_API_KEY.strip() if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip() else "NO_API_KEY_PROVIDED"
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=api_key,
            temperature=temperature,
            streaming=streaming,
        )
    elif provider == "nvidia":
        api_key = settings.NVIDIA_API_KEY.strip() if settings.NVIDIA_API_KEY and settings.NVIDIA_API_KEY.strip() else "NO_API_KEY_PROVIDED"
        return ChatOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
            model=settings.NVIDIA_MODEL,
            temperature=temperature,
            streaming=streaming,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
