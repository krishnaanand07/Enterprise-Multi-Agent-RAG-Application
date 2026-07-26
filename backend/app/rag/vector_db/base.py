"""
Base interface for vector database implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class BaseVectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        """Embeds and adds texts to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Searches for the most similar texts.
        Returns a list of tuples: (text, metadata, score)
        """
        pass
        
    @abstractmethod
    def delete_namespace(self, namespace: str) -> None:
        """Deletes all vectors associated with a specific namespace (e.g., user_id or document_id)."""
        pass
