"""
Hybrid Search Engine combining Dense (Vector) and Sparse (Keyword) search.
"""
from typing import List, Dict, Any
from app.rag.vector_db.faiss_store import faiss_store

class HybridSearchEngine:
    def __init__(self):
        self.vector_store = faiss_store

    def search(self, query: str, user_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a search using the vector store.
        (Future expansion: Add BM25 search and Reciprocal Rank Fusion here)
        """
        # Execute Semantic Search
        vector_results = self.vector_store.similarity_search(
            query=query, 
            namespace=user_id, 
            top_k=top_k
        )
        
        formatted_results = []
        for text, metadata, score in vector_results:
            formatted_results.append({
                "content": text,
                "metadata": metadata,
                "relevance_score": score,
                "source": "vector"
            })
            
        return formatted_results

search_engine = HybridSearchEngine()
