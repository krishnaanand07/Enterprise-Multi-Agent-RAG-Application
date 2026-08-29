"""
FAISS implementation of the vector store.
Uses LangChain's FAISS wrapper.
"""
import os
from typing import List, Dict, Any, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_community.vectorstores import FAISS

from app.rag.vector_db.base import BaseVectorStore
from app.config.settings import settings

import threading

class FAISSStore(BaseVectorStore):
    def __init__(self):
        self._embeddings = None
        self._lock = threading.Lock()
        self.storage_dir = "vector_db/faiss"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.indices = {} # In-memory cache of FAISS indices by namespace

    @property
    def embeddings(self):
        """Lazily load embeddings to save memory on startup (fixes Render 512MB RAM limit)."""
        if self._embeddings is None:
            with self._lock:
                if self._embeddings is None:
                    try:
                        if settings.GOOGLE_API_KEY:
                            from langchain_google_genai import GoogleGenerativeAIEmbeddings
                            self._embeddings = GoogleGenerativeAIEmbeddings(
                                model="models/text-embedding-004",
                                google_api_key=settings.GOOGLE_API_KEY
                            )
                        elif settings.OPENAI_API_KEY:
                            from langchain_openai import OpenAIEmbeddings
                            self._embeddings = OpenAIEmbeddings(
                                model="text-embedding-3-small",
                                openai_api_key=settings.OPENAI_API_KEY
                            )
                        elif settings.LLM_PROVIDER == "nvidia" and settings.NVIDIA_API_KEY:
                            from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
                            self._embeddings = NVIDIAEmbeddings(
                                model="nvidia/nv-embedqa-mistral-7b-v2",
                                nvidia_api_key=settings.NVIDIA_API_KEY
                            )
                        else:
                            from langchain_huggingface import HuggingFaceEmbeddings
                            self._embeddings = HuggingFaceEmbeddings(
                                model_name=settings.EMBEDDING_MODEL,
                                encode_kwargs={"batch_size": 32}
                            )
                    except Exception as e:
                        from loguru import logger
                        logger.warning(f"Failed to initialize primary embedding provider ({e}). Falling back to local HuggingFace embeddings.")
                        from langchain_huggingface import HuggingFaceEmbeddings
                        self._embeddings = HuggingFaceEmbeddings(
                            model_name=settings.EMBEDDING_MODEL,
                            encode_kwargs={"batch_size": 32}
                        )
        return self._embeddings

    def _get_index_path(self, namespace: str) -> str:
        return os.path.join(self.storage_dir, f"{namespace}.faiss")

    def _load_or_create_index(self, namespace: str) -> Any:
        if namespace in self.indices:
            return self.indices[namespace]
            
        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            from langchain_community.vectorstores import FAISS
            index = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            index = None
            
        if index:
            self.indices[namespace] = index
        return index

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        try:
            self._add_texts_internal(texts, metadatas, namespace)
        except Exception as e:
            from loguru import logger
            logger.warning(f"Primary embedding provider failed during add_texts ({e}). Falling back to local HuggingFace embeddings.")
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            self._add_texts_internal(texts, metadatas, namespace)

    def _add_texts_internal(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        index = self._load_or_create_index(namespace)

        if index is None:
            from langchain_community.vectorstores import FAISS
            index = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        else:
            index.add_texts(texts, metadatas=metadatas)

        # Save to disk
        index.save_local(self._get_index_path(namespace))
        self.indices[namespace] = index

    def similarity_search(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        try:
            return self._similarity_search_internal(query, namespace, top_k)
        except Exception as e:
            from loguru import logger
            logger.warning(f"Primary embedding provider failed during similarity_search ({e}). Falling back to local HuggingFace embeddings.")
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            return self._similarity_search_internal(query, namespace, top_k)

    def _similarity_search_internal(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        index = self._load_or_create_index(namespace)
        if not index:
            return []

        # FAISS returns (Document, score)
        results = index.similarity_search_with_score(query, k=top_k)

        # Normalize response
        return [(doc.page_content, doc.metadata, float(score)) for doc, score in results]

    def delete_document(self, document_id: str, namespace: str) -> None:
        index = self._load_or_create_index(namespace)
        if not index:
            return
            
        # Find all chunk IDs in FAISS docstore that belong to this document_id
        ids_to_delete = []
        if hasattr(index, "docstore") and hasattr(index.docstore, "_dict"):
            for faiss_id, doc in index.docstore._dict.items():
                if doc.metadata.get("document_id") == document_id:
                    ids_to_delete.append(faiss_id)
        
        if ids_to_delete:
            index.delete(ids_to_delete)
            # Save to disk
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
