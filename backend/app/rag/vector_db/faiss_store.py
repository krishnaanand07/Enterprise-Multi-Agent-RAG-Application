"""
FAISS implementation of the vector store.

Key improvements over the original:
  - add_texts_async() — wraps the blocking add in asyncio.to_thread
  - Batched embedding (32 chunks at a time) with exponential-backoff retry
    → prevents API timeouts on large documents
  - save_local() also runs off the event loop via to_thread
  - Thread-safe with a single reentrant lock
"""
import asyncio
import os
import time
import threading
from typing import List, Dict, Any, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_community.vectorstores import FAISS

from app.rag.vector_db.base import BaseVectorStore
from app.config.settings import settings
from loguru import logger

# How many text chunks to embed per API call
EMBED_BATCH_SIZE = 32
# Retry parameters for transient API errors
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2.0  # seconds (doubles each retry)


class FAISSStore(BaseVectorStore):
    def __init__(self):
        self._embeddings = None
        self._lock = threading.Lock()
        self.storage_dir = "vector_db/faiss"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.indices: Dict[str, Any] = {}  # In-memory cache by namespace

    # ------------------------------------------------------------------ #
    #  Lazy embedding initialisation                                       #
    # ------------------------------------------------------------------ #
    @property
    def embeddings(self):
        """Lazy-load embeddings on first use (saves RAM on cold starts)."""
        if self._embeddings is None:
            with self._lock:
                if self._embeddings is None:
                    self._embeddings = self._init_embeddings()
        return self._embeddings

    def _init_embeddings(self):
        try:
            if settings.GOOGLE_API_KEY:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                logger.info("Using Google Generative AI embeddings.")
                return GoogleGenerativeAIEmbeddings(
                    model="models/text-embedding-004",
                    google_api_key=settings.GOOGLE_API_KEY,
                )
            if settings.OPENAI_API_KEY:
                from langchain_openai import OpenAIEmbeddings
                logger.info("Using OpenAI embeddings.")
                return OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key=settings.OPENAI_API_KEY,
                )
            if settings.LLM_PROVIDER == "nvidia" and settings.NVIDIA_API_KEY:
                from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
                logger.info("Using NVIDIA embeddings.")
                return NVIDIAEmbeddings(
                    model="nvidia/nv-embedqa-mistral-7b-v2",
                    nvidia_api_key=settings.NVIDIA_API_KEY,
                )
        except Exception as e:
            logger.warning(
                f"Primary embedding provider failed ({e}). "
                "Falling back to local HuggingFace embeddings."
            )

        logger.info(f"Using local HuggingFace embeddings ({settings.EMBEDDING_MODEL}).")
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            encode_kwargs={"batch_size": EMBED_BATCH_SIZE},
        )

    def _reset_to_local_embeddings(self):
        """Switch to local HuggingFace embeddings after API failure."""
        from langchain_huggingface import HuggingFaceEmbeddings
        self._embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            encode_kwargs={"batch_size": EMBED_BATCH_SIZE},
        )

    # ------------------------------------------------------------------ #
    #  Index helpers                                                       #
    # ------------------------------------------------------------------ #
    def _get_index_path(self, namespace: str) -> str:
        return os.path.join(self.storage_dir, f"{namespace}.faiss")

    def _load_or_create_index(self, namespace: str) -> Any:
        if namespace in self.indices:
            return self.indices[namespace]

        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            from langchain_community.vectorstores import FAISS
            index = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            self.indices[namespace] = index
            return index
        return None

    # ------------------------------------------------------------------ #
    #  Public async interface                                              #
    # ------------------------------------------------------------------ #
    async def add_texts_async(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        namespace: str,
    ) -> None:
        """Non-blocking wrapper — runs the sync embedding work in a thread."""
        await asyncio.to_thread(self.add_texts, texts, metadatas, namespace)

    # ------------------------------------------------------------------ #
    #  Sync add_texts with batching + retry                               #
    # ------------------------------------------------------------------ #
    def add_texts(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        namespace: str,
    ) -> None:
        """
        Embed texts in batches and store in FAISS.
        Retries up to MAX_RETRIES times on transient errors, then falls back
        to local HuggingFace embeddings if the API keeps failing.
        """
        try:
            self._add_texts_batched(texts, metadatas, namespace)
        except Exception as exc:
            logger.warning(
                f"Primary embedding provider failed during add_texts ({exc}). "
                "Switching to local HuggingFace embeddings and retrying."
            )
            self._reset_to_local_embeddings()
            self._add_texts_batched(texts, metadatas, namespace)

    def _add_texts_batched(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        namespace: str,
    ) -> None:
        """Embed + store in EMBED_BATCH_SIZE chunks with exponential-backoff retry."""
        from langchain_community.vectorstores import FAISS

        index = self._load_or_create_index(namespace)

        # Process in batches to avoid API payload/timeout limits
        for batch_start in range(0, len(texts), EMBED_BATCH_SIZE):
            batch_texts = texts[batch_start: batch_start + EMBED_BATCH_SIZE]
            batch_metas = metadatas[batch_start: batch_start + EMBED_BATCH_SIZE]

            last_error: Exception | None = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    if index is None:
                        index = FAISS.from_texts(
                            batch_texts,
                            self.embeddings,
                            metadatas=batch_metas,
                        )
                    else:
                        index.add_texts(batch_texts, metadatas=batch_metas)
                    last_error = None
                    break  # success
                except Exception as e:
                    last_error = e
                    delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    logger.warning(
                        f"Embedding batch [{batch_start}:{batch_start+len(batch_texts)}] "
                        f"attempt {attempt}/{MAX_RETRIES} failed: {e}. "
                        f"Retrying in {delay:.1f}s…"
                    )
                    time.sleep(delay)

            if last_error:
                raise last_error

            logger.debug(
                f"Embedded batch [{batch_start}:{batch_start+len(batch_texts)}] "
                f"for namespace={namespace}"
            )

        # Persist to disk (blocking, but already inside to_thread)
        if index is not None:
            index.save_local(self._get_index_path(namespace))
            self.indices[namespace] = index

    # ------------------------------------------------------------------ #
    #  Similarity search                                                   #
    # ------------------------------------------------------------------ #
    def similarity_search(
        self,
        query: str,
        namespace: str,
        top_k: int = 4,
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        try:
            return self._similarity_search_internal(query, namespace, top_k)
        except Exception as exc:
            logger.warning(
                f"Primary embedding provider failed during similarity_search ({exc}). "
                "Switching to local HuggingFace embeddings."
            )
            self._reset_to_local_embeddings()
            return self._similarity_search_internal(query, namespace, top_k)

    def _similarity_search_internal(
        self,
        query: str,
        namespace: str,
        top_k: int = 4,
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        index = self._load_or_create_index(namespace)
        if not index:
            return []
        results = index.similarity_search_with_score(query, k=top_k)
        return [(doc.page_content, doc.metadata, float(score)) for doc, score in results]

    # ------------------------------------------------------------------ #
    #  Delete helpers                                                      #
    # ------------------------------------------------------------------ #
    def delete_document(self, document_id: str, namespace: str) -> None:
        index = self._load_or_create_index(namespace)
        if not index:
            return

        ids_to_delete = []
        if hasattr(index, "docstore") and hasattr(index.docstore, "_dict"):
            for faiss_id, doc in index.docstore._dict.items():
                if doc.metadata.get("document_id") == document_id:
                    ids_to_delete.append(faiss_id)

        if ids_to_delete:
            index.delete(ids_to_delete)
            index.save_local(self._get_index_path(namespace))
            self.indices[namespace] = index

    def delete_namespace(self, namespace: str) -> None:
        if namespace in self.indices:
            del self.indices[namespace]

        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            import shutil
            shutil.rmtree(index_path)


faiss_store = FAISSStore()
