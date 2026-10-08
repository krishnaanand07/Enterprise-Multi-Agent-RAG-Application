"""
Unit tests for component architecture integrity.
"""
import pytest
from app.agents.supervisor import SupervisorAgent
from app.agents.rag_agent import RAGAgent
from app.agents.data_agent import DataAgent
from app.agents.general_agent import GeneralAgent
from app.rag.vector_store import VectorStoreManager

def test_supervisor_agent_routing_structure():
    """Verify SupervisorAgent prompt and route function signature."""
    assert hasattr(SupervisorAgent, "route")
    assert "DOCUMENT" in SupervisorAgent.SUPERVISOR_PROMPT

def test_agents_callable():
    """Verify agent process methods exist."""
    assert hasattr(RAGAgent, "process")
    assert hasattr(DataAgent, "process")
    assert hasattr(GeneralAgent, "process")

def test_vector_store_lazy_initialization():
    """Verify VectorStoreManager initializes cleanly."""
    manager = VectorStoreManager()
    assert manager is not None
