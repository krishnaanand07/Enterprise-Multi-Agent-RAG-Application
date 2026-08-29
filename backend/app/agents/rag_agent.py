"""
The RAG Agent Node. Retrieves context and answers questions.
"""
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import AgentState
from app.rag.search.hybrid_search import search_engine
from app.services.langchain_llm import get_llm

import threading

class RAGAgent:
    def __init__(self):
        self._llm = None
        self._lock = threading.Lock()

    @property
    def llm(self):
        if self._llm is None:
            with self._lock:
                if self._llm is None:
                    self._llm = get_llm(temperature=0.0) # Low temperature for factual RAG
        return self._llm
        
    async def retrieve_node(self, state: AgentState) -> dict:
        """Retrieves documents from the vector database."""
        logger.info(f"RAG Agent: Retrieving context for query: {state['question']}")
        
        results = search_engine.search(
            query=state["question"], 
            user_id=state["user_id"], 
            top_k=5
        )
        
        return {"retrieved_documents": results}
        
    async def generate_node(self, state: AgentState) -> dict:
        """Generates an answer based on retrieved documents."""
        logger.info("RAG Agent: Generating answer from context.")
        
        docs = state.get("retrieved_documents", [])
        
        if not docs:
            return {
                "final_answer": "I couldn't find any relevant information in your uploaded documents to answer that question.",
                "citations": []
            }
            
        # Format context
        context_str = ""
        citations = []
        for i, doc in enumerate(docs):
            content = doc.get("content", "")
            meta = doc.get("metadata", {})
            filename = meta.get("filename", "Unknown")
            
            context_str += f"\n\n--- Source [{i+1}] ({filename}) ---\n{content}\n"
            
            citations.append({
                "document_name": filename,
                "chunk_text": content[:200] + "...",
                "relevance_score": doc.get("relevance_score", 0.0)
            })

        system_prompt = (
            "You are an expert research assistant. Answer the user's question using ONLY the provided context.\n"
            "If the context does not contain the answer, say 'I cannot answer this based on the provided documents.'\n"
            "Use markdown formatting. Always cite your sources using the Source number, e.g., [1]."
        )
        
        human_prompt = f"Context:\n{context_str}\n\nQuestion: {state['question']}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "final_answer": response.content,
            "citations": citations
        }

rag_agent = RAGAgent()
