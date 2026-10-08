from typing import List, Dict, Any, Optional, Tuple
from langchain_core.documents import Document as LCDocument
from app.rag.vector_store import VectorStoreManager


class DocumentRetriever:
    """Document Retriever handling vector search and citation formatting."""

    @staticmethod
    def retrieve_context(
        user_id: str, 
        query: str, 
        top_k: int = 4, 
        document_id: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Retrieves top-k relevant document chunks.
        Returns:
            Tuple of (formatted_context_string, list_of_citation_dicts)
        """
        retrieved_docs: List[LCDocument] = VectorStoreManager.similarity_search(
            user_id=user_id,
            query=query,
            top_k=top_k,
            document_id=document_id
        )

        if not retrieved_docs:
            return "", []

        context_parts = []
        sources: List[Dict[str, Any]] = []
        seen_chunks = set()

        for idx, doc in enumerate(retrieved_docs):
            content = doc.page_content
            meta = doc.metadata
            doc_name = meta.get("document_name", "Unknown Document")
            page_num = meta.get("page_number", 1)
            chunk_id = meta.get("chunk_id", f"chunk_{idx}")

            context_parts.append(f"[Source {idx+1}: {doc_name} (Page {page_num})]\n{content}")

            if chunk_id not in seen_chunks:
                seen_chunks.add(chunk_id)
                sources.append({
                    "document_id": meta.get("document_id", ""),
                    "document_name": doc_name,
                    "page_number": page_num,
                    "chunk_id": chunk_id,
                    "source_type": meta.get("source_type", "pdf"),
                    "snippet": content[:200] + "..." if len(content) > 200 else content
                })

        formatted_context = "\n\n".join(context_parts)
        return formatted_context, sources
