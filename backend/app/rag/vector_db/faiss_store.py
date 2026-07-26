"""
FAISS implementation of the vector store.
Uses LangChain's FAISS wrapper.
"""
import os
from typing import List, Dict, Any, Tuple
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.rag.vector_db.base import BaseVectorStore
from app.config.settings import settings

class FAISSStore(BaseVectorStore):
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.storage_dir = "vector_db/faiss"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.indices = {} # In-memory cache of FAISS indices by namespace

    def _get_index_path(self, namespace: str) -> str:
        return os.path.join(self.storage_dir, f"{namespace}.faiss")

    def _load_or_create_index(self, namespace: str) -> FAISS:
        if namespace in self.indices:
            return self.indices[namespace]
            
        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            index = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            index = None
            
        if index:
            self.indices[namespace] = index
        return index

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        index = self._load_or_create_index(namespace)
        
        if index is None:
            index = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        else:
            index.add_texts(texts, metadatas=metadatas)
            
        # Save to disk
        index.save_local(self._get_index_path(namespace))
        self.indices[namespace] = index

    def similarity_search(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        index = self._load_or_create_index(namespace)
        if not index:
            return []
            
        # FAISS returns (Document, score)
        results = index.similarity_search_with_score(query, k=top_k)
        
        # Normalize response
        return [(doc.page_content, doc.metadata, float(score)) for doc, score in results]

    def delete_namespace(self, namespace: str) -> None:
        if namespace in self.indices:
            del self.indices[namespace]
        
        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            import shutil
            shutil.rmtree(index_path)

faiss_store = FAISSStore()
