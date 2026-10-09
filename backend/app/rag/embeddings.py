import logging
import os
from functools import lru_cache
from langchain_core.embeddings import Embeddings

from app.core.config import settings

logger = logging.getLogger("enterprise_rag")


def _sanitize_error(error: Exception, api_key: str = "") -> str:
    """Removes API key from error message string to prevent sensitive leak in logs."""
    msg = str(error)
    if api_key and api_key in msg:
        msg = msg.replace(api_key, "[REDACTED]")
    return msg


@lru_cache(maxsize=1)
def get_embeddings_model() -> Embeddings:
    """
    Returns initialized Embeddings model instance (singleton).
    Uses GoogleGenerativeAIEmbeddings in production when GEMINI_API_KEY is configured.
    In production mode, fails fast if API key is missing/invalid or init fails. Never loads PyTorch/HF in prod.
    Falls back to single-threaded CPU HuggingFaceEmbeddings only in development/test environments.
    """
    api_key = settings.GEMINI_API_KEY
    is_production = settings.ENVIRONMENT.lower() == "production"

    if is_production:
        if not api_key or api_key.startswith("dummy"):
            logger.error("Production error: GEMINI_API_KEY is missing or invalid in production environment.")
            raise RuntimeError("GEMINI_API_KEY must be configured with a valid key in production environment.")

        try:
            logger.info("Model loading: Initializing remote GoogleGenerativeAIEmbeddings ('gemini-embedding-001') in production...")
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            model = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=api_key
            )
            logger.info("Model loaded: Remote GoogleGenerativeAIEmbeddings initialized successfully.")
            return model
        except Exception as e:
            safe_err = _sanitize_error(e, api_key)
            logger.error(f"Failed to initialize remote GoogleGenerativeAIEmbeddings in production: {safe_err}")
            raise RuntimeError(f"Failed to initialize remote GoogleGenerativeAIEmbeddings in production: {safe_err}") from e

    # Non-production (development / testing environment):
    if api_key and not api_key.startswith("dummy"):
        try:
            logger.info("Model loading: Initializing remote GoogleGenerativeAIEmbeddings ('gemini-embedding-001')...")
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            model = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=api_key
            )
            logger.info("Model loaded: Remote GoogleGenerativeAIEmbeddings initialized successfully.")
            return model
        except Exception as e:
            safe_err = _sanitize_error(e, api_key)
            logger.error(f"Failed to initialize remote GoogleGenerativeAIEmbeddings: {safe_err}")
            raise RuntimeError(f"Failed to initialize remote GoogleGenerativeAIEmbeddings: {safe_err}") from e

    logger.info(f"Model loading: Loading local embedding model '{settings.EMBEDDING_MODEL}' on CPU (1 thread)...")
    try:
        try:
            import torch
            torch.set_num_threads(1)
            if hasattr(torch, "set_num_interop_threads"):
                torch.set_num_interop_threads(1)
        except Exception:
            pass

        from langchain_community.embeddings import HuggingFaceEmbeddings
        model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info(f"Model loaded: Local embedding model '{settings.EMBEDDING_MODEL}' loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize local HuggingFaceEmbeddings model '{settings.EMBEDDING_MODEL}': {str(e)}")
        raise RuntimeError(f"Failed to initialize local HuggingFaceEmbeddings model: {str(e)}") from e
