from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.rag.retriever import DocumentRetriever
from app.services.llm_service import llm_service


class RAGAgent:
    """RAG Agent for vector retrieval and grounded context synthesis."""

    RAG_SYSTEM_PROMPT = """You are an Enterprise Document AI Assistant.
Answer the user's question accurately based ONLY on the provided context chunks below.

Rules:
1. Ground your answer strictly in the provided context.
2. If the context does not contain enough information to answer the question, state clearly: "I could not find relevant information in your uploaded enterprise documents to answer this question."
3. Keep your response professional, well-structured, and concise.

Context Chunks:
{context}

Question: {query}
Answer:"""

    @classmethod
    async def process(cls, state: AgentState) -> AgentState:
        query = state["query"]
        user_id = state["user_id"]
        selected_doc_id = state.get("selected_document_id")

        # Step 1: Retrieve context (with document scoping if selected)
        context_text, sources = DocumentRetriever.retrieve_context(
            user_id=user_id,
            query=query,
            top_k=4,
            document_id=selected_doc_id
        )

        if not context_text:
            state["response"] = "No matching information found in your uploaded enterprise documents."
            state["sources"] = []
            state["agent_used"] = "RAG Agent"
            return state

        # Step 2: Gemini Generation
        try:
            llm = llm_service.get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_template(cls.RAG_SYSTEM_PROMPT)
            chain = prompt | llm
            res = await chain.ainvoke({
                "context": context_text,
                "query": query
            })
            state["response"] = str(res.content).strip()
            state["sources"] = sources
            state["agent_used"] = "RAG Agent"
        except Exception as e:
            state["response"] = f"Error generating answer: {str(e)}"
            state["sources"] = sources
            state["agent_used"] = "RAG Agent"

        return state
