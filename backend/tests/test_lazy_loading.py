"""
Unit tests for lazy loading component integrity.
"""
import pytest
from app.agents.supervisor import SupervisorAgent
from app.agents.rag_agent import RAGAgent
from app.agents.sql_agent import SQLAgent
from app.rag.vector_db.faiss_store import FAISSStore

def test_supervisor_lazy_loading():
    """Verify SupervisorAgent initializes without eager LLM or Graph compilation."""
    agent = SupervisorAgent()
    assert agent._llm is None
    assert agent._graph is None
    # Access properties lazily
    assert agent.llm is not None
    assert agent.graph is not None
    assert agent._llm is not None
    assert agent._graph is not None

def test_rag_agent_lazy_loading():
    """Verify RAGAgent initializes lazily."""
    agent = RAGAgent()
    assert agent._llm is None
    assert agent.llm is not None
    assert agent._llm is not None

def test_sql_agent_lazy_loading():
    """Verify SQLAgent initializes lazily."""
    agent = SQLAgent()
    assert agent._llm is None
    assert agent.llm is not None
    assert agent._llm is not None

def test_faiss_store_lazy_loading():
    """Verify FAISSStore initializes lazily without throwing import errors."""
    store = FAISSStore()
    assert store._embeddings is None
    assert store.indices == {}
