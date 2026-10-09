import os
import shutil
import logging
import threading
from typing import Dict, List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LCDocument

from app.core.config import settings
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger("enterprise_rag")


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
        except Exception:
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
                    new_store.save_local(index_path)
                else:
                    shutil.rmtree(index_path, ignore_errors=True)

                return True
            except Exception:
                return False
