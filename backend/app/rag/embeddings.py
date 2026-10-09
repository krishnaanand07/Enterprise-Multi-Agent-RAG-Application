import logging
from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings

from app.core.config import settings

logger = logging.getLogger("enterprise_rag")


@lru_cache(maxsize=1)
def get_embeddings_model() -> Embeddings:
    """
    Returns initialized HuggingFace Embeddings model instance (singleton).
    Uses sentence-transformers/all-MiniLM-L6-v2.
    """
    logger.info(f"Model loading: Loading embedding model '{settings.EMBEDDING_MODEL}' on CPU...")
    model = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    logger.info(f"Model loaded: Embedding model '{settings.EMBEDDING_MODEL}' loaded successfully.")
    return model

