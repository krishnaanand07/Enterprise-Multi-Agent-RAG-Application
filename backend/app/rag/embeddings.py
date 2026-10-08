from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings

from app.core.config import settings


def get_embeddings_model() -> Embeddings:
    """
    Returns initialized HuggingFace Embeddings model instance.
    Uses sentence-transformers/all-MiniLM-L6-v2.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
