import os
import json
import shutil
import logging
import threading
from typing import Dict, List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LCDocument

from app.core.config import settings
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger("enterprise_rag")


def _get_model_identity(embeddings) -> str:
    """Extracts unique model identifier string from Embeddings instance."""
    if hasattr(embeddings, "model") and embeddings.model:
        return str(embeddings.model)
    if hasattr(embeddings, "model_name") and embeddings.model_name:
        return str(embeddings.model_name)
    return embeddings.__class__.__name__


def _save_index_metadata(index_path: str, model_id: str, dimension: int) -> None:
    """
    Saves model identity and dimension metadata alongside FAISS index files.
    Fails cleanly if file write fails without destroying existing FAISS index data.
    """
    meta_path = os.path.join(index_path, "index_metadata.json")
    data = {
        "embedding_model": model_id,
        "embedding_dimension": dimension,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _validate_index_compatibility(index_path: str, embeddings) -> None:
    """
    Validates model identity and embedding dimension compatibility of existing FAISS index.
    Refuses operation if index lacks metadata or has incompatible model/dimension.
    Never deletes or alters existing index files.
    """
    meta_path = os.path.join(index_path, "index_metadata.json")
    sample_vec = embeddings.embed_query("dimension_check")
    current_dim = len(sample_vec)
    current_model = _get_model_identity(embeddings)

    if not os.path.exists(meta_path):
        msg = (
            f"FAISS index at {index_path} lacks verified model metadata (legacy or unverified embedding model). "
            f"Refusing operation with active model '{current_model}'. Controlled re-embedding of existing documents is required. "
            f"Existing index at {index_path} was preserved."
        )
        logger.error(f"Vector store compatibility error: {msg}")
        raise ValueError(msg)

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        msg = (
            f"Failed to read FAISS index metadata at {meta_path}: {str(e)}. "
            f"Existing index at {index_path} was preserved."
        )
        logger.error(f"Vector store metadata read error: {msg}")
        raise ValueError(msg) from e

    stored_model = meta.get("embedding_model")
    stored_dim = meta.get("embedding_dimension")

    if stored_model != current_model or stored_dim != current_dim:
        msg = (
            f"FAISS index model identity/dimension mismatch (stored: '{stored_model}', dim {stored_dim}) "
            f"vs active embedding model (current: '{current_model}', dim {current_dim}). "
            f"Controlled re-embedding of existing documents is required for model migration. "
            f"Existing index at {index_path} was preserved."
        )
        logger.error(f"Vector store compatibility error: {msg}")
        raise ValueError(msg)


class VectorStoreManager:
    """FAISS Vector Store Manager with user path isolation and per-user thread locks."""

    _user_locks: Dict[str, threading.Lock] = {}
    _global_lock = threading.Lock()

    @classmethod
    def _get_user_lock(cls, user_id: str) -> threading.Lock:
        with cls._global_lock:
            if user_id not in cls._user_locks:
                cls._user_locks[user_id] = threading.Lock()
            return cls._user_locks[user_id]

    @staticmethod
    def _get_user_index_path(user_id: str) -> str:
        return os.path.join(settings.VECTOR_STORE_DIR, f"user_{user_id}")

    @classmethod
    def add_documents(cls, user_id: str, documents: List[LCDocument]) -> bool:
        if not documents:
            return False

        user_lock = cls._get_user_lock(user_id)
        with user_lock:
            index_path = cls._get_user_index_path(user_id)
            os.makedirs(index_path, exist_ok=True)
            embeddings = get_embeddings_model()

            try:
                if os.path.exists(os.path.join(index_path, "index.faiss")):
                    logger.info(f"Vector indexing: Validating compatibility for existing FAISS index at {index_path}...")
                    _validate_index_compatibility(index_path, embeddings)

                    logger.info(f"Vector indexing: Loading existing FAISS index from {index_path}...")
                    vector_store = FAISS.load_local(
                        index_path,
                        embeddings,
                        allow_dangerous_deserialization=True
                    )

                    logger.info(f"Vector indexing: Adding {len(documents)} document chunks to FAISS index...")
                    vector_store.add_documents(documents)
                else:
                    logger.info(f"Vector indexing: Creating new FAISS index for {len(documents)} document chunks...")
                    vector_store = FAISS.from_documents(documents, embeddings)

                sample_vec = embeddings.embed_query("dimension_check")
                _save_index_metadata(index_path, _get_model_identity(embeddings), len(sample_vec))

                logger.info(f"Vector indexing: Saving FAISS index to {index_path}...")
                vector_store.save_local(index_path)
                logger.info(f"Vector indexing: Vector store persistence complete at {index_path}.")
                return True
            except Exception as e:
                logger.error(f"Vector indexing error for user {user_id}: {str(e)}", exc_info=True)
                raise e

    @classmethod
    def similarity_search(
        cls, 
        user_id: str, 
        query: str, 
        top_k: int = 4, 
        document_id: Optional[str] = None
    ) -> List[LCDocument]:
        index_path = cls._get_user_index_path(user_id)
        if not os.path.exists(os.path.join(index_path, "index.faiss")):
            return []

        try:
            embeddings = get_embeddings_model()
            _validate_index_compatibility(index_path, embeddings)

            vector_store = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )

            filter_dict = {"document_id": str(document_id)} if document_id else None
            
            docs = vector_store.similarity_search(
                query, 
                k=top_k, 
                filter=filter_dict
            )
            return docs
        except Exception as e:
            logger.error(f"Error during FAISS similarity search for user {user_id}: {str(e)}")
            return []

    @classmethod
    def delete_document(cls, user_id: str, document_id: str) -> bool:
        user_lock = cls._get_user_lock(user_id)
        with user_lock:
            index_path = cls._get_user_index_path(user_id)
            if not os.path.exists(os.path.join(index_path, "index.faiss")):
                return True

            try:
                embeddings = get_embeddings_model()
                _validate_index_compatibility(index_path, embeddings)

                vector_store = FAISS.load_local(
                    index_path,
                    embeddings,
                    allow_dangerous_deserialization=True
                )

                all_docs = list(vector_store.docstore._dict.values())
                remaining_docs = [
                    d for d in all_docs
                    if d.metadata.get("document_id") != str(document_id)
                ]

                if remaining_docs:
                    new_store = FAISS.from_documents(remaining_docs, embeddings)
                    sample_vec = embeddings.embed_query("dimension_check")
                    _save_index_metadata(index_path, _get_model_identity(embeddings), len(sample_vec))
                    new_store.save_local(index_path)
                else:
                    shutil.rmtree(index_path, ignore_errors=True)

                return True
            except Exception as e:
                logger.error(f"FAISS delete_document failed for user {user_id}: {str(e)}")
                return False
