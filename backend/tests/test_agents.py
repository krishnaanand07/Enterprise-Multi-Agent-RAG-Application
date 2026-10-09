import pytest
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage

from app.rag.chunker import DocumentChunker
from app.agents.supervisor import SupervisorAgent
from app.agents.rag_agent import RAGAgent
from app.agents.graph import run_agent_workflow
from app.rag.retriever import DocumentRetriever
import app.services.llm_service as llm_service_module


def test_document_chunker_metadata():
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    pages = [
        {"content": "This is page one of the enterprise handbook containing policy details.", "page_number": 1},
        {"content": "This is page two containing financial reporting information.", "page_number": 2}
    ]
    chunks = chunker.chunk_document(pages, "doc_123", "handbook.pdf", "user_abc")

    assert len(chunks) > 0
    first_chunk = chunks[0]
    assert first_chunk.metadata["document_id"] == "doc_123"
    assert first_chunk.metadata["document_name"] == "handbook.pdf"
    assert first_chunk.metadata["user_id"] == "user_abc"
    assert "page_number" in first_chunk.metadata


@pytest.mark.asyncio
async def test_supervisor_routes_pilot_budget_to_document(monkeypatch):
    """Verify 'What is Northstar's total pilot budget?' routes to DOCUMENT (RAG Agent)."""
    mock_llm = RunnableLambda(lambda x: AIMessage(content="DOCUMENT"))
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", lambda **kwargs: mock_llm)

    state = {
        "query": "What is Northstar's total pilot budget?",
        "user_id": "test_user",
        "conversation_id": "conv_1"
    }
    result = await SupervisorAgent.route(state)
    assert result["route"] == "DOCUMENT"


@pytest.mark.asyncio
async def test_supervisor_routes_p1_support_target_to_document(monkeypatch):
    """Verify 'What is the P1 support acknowledgement target?' routes to DOCUMENT (RAG Agent)."""
    mock_llm = RunnableLambda(lambda x: AIMessage(content="DOCUMENT"))
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", lambda **kwargs: mock_llm)

    state = {
        "query": "What is the P1 support acknowledgement target?",
        "user_id": "test_user",
        "conversation_id": "conv_1"
    }
    result = await SupervisorAgent.route(state)
    assert result["route"] == "DOCUMENT"


@pytest.mark.asyncio
async def test_supervisor_routes_csv_analysis_to_data(monkeypatch):
    """Verify explicit CSV requests route to DATA (Data Agent)."""
    mock_llm = RunnableLambda(lambda x: AIMessage(content="DATA"))
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", lambda **kwargs: mock_llm)

    state = {
        "query": "Analyze my uploaded CSV and calculate average revenue",
        "user_id": "test_user",
        "conversation_id": "conv_1"
    }
    result = await SupervisorAgent.route(state)
    assert result["route"] == "DATA"


@pytest.mark.asyncio
async def test_supervisor_prevents_misrouting_numerical_document_query_to_data(monkeypatch):
    """Verify that even if LLM classifies a document budget query as DATA, supervisor enforces DOCUMENT route."""
    mock_llm = RunnableLambda(lambda x: AIMessage(content="DATA"))
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", lambda **kwargs: mock_llm)

    state = {
        "query": "What is Northstar's total pilot budget?",
        "user_id": "test_user",
        "conversation_id": "conv_1"
    }
    result = await SupervisorAgent.route(state)
    assert result["route"] == "DOCUMENT"


@pytest.mark.asyncio
async def test_rag_agent_workflow_pilot_budget_grounded_answer(monkeypatch):
    """Verify Northstar pilot budget query retrieves document context and returns answer ₹450,000."""
    def mock_retrieve_context(user_id, query, top_k=4, document_id=None):
        return (
            "Document: Project Northstar Charter. Page 3. Northstar's total pilot budget is ₹450,000 for Q3 execution.",
            [{
                "document_id": "doc_northstar",
                "document_name": "northstar_charter.pdf",
                "page_number": 3,
                "chunk_id": "chunk_1",
                "snippet": "Northstar's total pilot budget is ₹450,000 for Q3 execution."
            }]
        )

    mock_supervisor_llm = RunnableLambda(lambda x: AIMessage(content="DOCUMENT"))
    mock_rag_llm = RunnableLambda(lambda x: AIMessage(content="Northstar's total pilot budget is ₹450,000."))

    def mock_get_llm(**kwargs):
        if kwargs.get("temperature") == 0.0:
            return mock_supervisor_llm
        return mock_rag_llm

    monkeypatch.setattr(DocumentRetriever, "retrieve_context", mock_retrieve_context)
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", mock_get_llm)

    result = await run_agent_workflow(
        query="What is Northstar's total pilot budget?",
        user_id="test_user",
        conversation_id="conv_1"
    )

    assert result["agent_used"] == "RAG Agent"
    assert "₹450,000" in result["response"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["document_name"] == "northstar_charter.pdf"


@pytest.mark.asyncio
async def test_rag_agent_workflow_no_relevant_evidence(monkeypatch):
    """Verify query with no relevant document context produces clear insufficient-evidence response without hallucination."""
    def mock_empty_context(user_id, query, top_k=4, document_id=None):
        return ("", [])

    mock_supervisor_llm = RunnableLambda(lambda x: AIMessage(content="DOCUMENT"))
    monkeypatch.setattr(DocumentRetriever, "retrieve_context", mock_empty_context)
    monkeypatch.setattr(llm_service_module.llm_service, "get_llm", lambda **kwargs: mock_supervisor_llm)

    result = await run_agent_workflow(
        query="What is the secret launch date of Project Apollo 13?",
        user_id="test_user",
        conversation_id="conv_1"
    )

    assert result["agent_used"] == "RAG Agent"
    assert "could not find relevant information" in result["response"].lower() or "no matching information" in result["response"].lower()
    assert result["sources"] == []
