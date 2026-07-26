"""
Embedding service using HuggingFace Sentence Transformers.

Converts text into numerical vectors for semantic search.
The model is loaded once at startup and reused for all requests.

Usage:
    from app.rag.embeddings.embedding_service import embedding_service

    vector = embedding_service.embed_text("Hello world")
    vectors = embedding_service.embed_batch(["text1", "text2"])
"""

from typing import List
import numpy as np
from loguru import logger

from app.config.settings import settings


class EmbeddingService:
    """
    Manages text embedding using HuggingFace Sentence Transformers.
    """

    def __init__(self):
        self._model = None
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION

    def _load_model(self):
        """Load the embedding model into memory."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info(
                f"Embedding model loaded. Dimension: {self.dimension}"
            )
        return self._model

    def embed_text(self, text: str) -> np.ndarray:
        """
        Convert a single text string into an embedding vector.

        Returns:
            numpy array of shape (384,) for MiniLM-L6-v2.
        """
        model = self._load_model()
        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embedding

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 64,
        show_progress: bool = False,
    ) -> np.ndarray:
        """
        Convert a batch of texts into embedding vectors.

        Returns:
            numpy array of shape (len(texts), 384).
        """
        model = self._load_model()
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=show_progress,
        )
        logger.info(f"Embedded {len(texts)} texts → shape {embeddings.shape}")
        return embeddings

    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.

        Returns:
            Float between -1.0 and 1.0 (1.0 = identical meaning).
        """
        vec1 = self.embed_text(text1)
        vec2 = self.embed_text(text2)
        return float(np.dot(vec1, vec2))


# Singleton instance
embedding_service = EmbeddingService()
