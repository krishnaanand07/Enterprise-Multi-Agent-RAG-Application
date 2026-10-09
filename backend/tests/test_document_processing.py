"""
Unit tests for Document Ingestion Pipeline, Embedding Model Caching, and Background Exception Handling.
"""
import os
import json
import pytest
import uuid
import app.rag.embeddings as embeddings_module
import app.database.database as db_module
import app.services.document_service as doc_service_module
from app.rag.embeddings import get_embeddings_model
from app.services.document_service import DocumentService
from app.models import Document
from app.database.database import Base
from sqlalchemy.future import select
from langchain_core.documents import Document as LCDocument
from app.rag.vector_store import VectorStoreManager, _save_index_metadata

_ORIGINAL_ADD_DOCUMENTS = VectorStoreManager.__dict__["add_documents"]


class _StubHuggingFaceEmbeddings:
    """Stub for HuggingFaceEmbeddings to prevent loading PyTorch weights or model files."""
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs.get("model_name", "stub-hf")

    def embed_documents(self, texts):
        return [[0.0] * 384 for _ in texts]

    def embed_query(self, text):
        return [0.0] * 384


class _StubGoogleEmbeddings:
    """Stub for GoogleGenerativeAIEmbeddings to prevent remote API calls in unit tests."""
    def __init__(self, model="gemini-embedding-001", google_api_key=None, **kwargs):
        self.model = model
        self.google_api_key = google_api_key

    def embed_documents(self, texts):
        return [[0.0] * 768 for _ in texts]

    def embed_query(self, text):
        return [0.0] * 768


@pytest.fixture(autouse=True)
def mock_embedding_and_vectorstore(monkeypatch):
    """Global fixture for test_document_processing.py that mocks embedding constructors and FAISS vector store."""
    import langchain_community.embeddings
    import langchain_google_genai

    monkeypatch.setattr(
        langchain_community.embeddings,
        "HuggingFaceEmbeddings",
        _StubHuggingFaceEmbeddings
    )
    monkeypatch.setattr(
        langchain_google_genai,
        "GoogleGenerativeAIEmbeddings",
        _StubGoogleEmbeddings
    )
    monkeypatch.setattr(
        doc_service_module.VectorStoreManager,
        "add_documents",
        lambda user_id, documents: True
    )

    get_embeddings_model.cache_clear()
    yield
    get_embeddings_model.cache_clear()


@pytest.fixture(autouse=True)
async def setup_test_schema():
    """Initializes schema in database for test execution."""
    async with db_module.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


def test_embeddings_model_caching():
    """Verify get_embeddings_model uses lru_cache singleton."""
    get_embeddings_model.cache_clear()
    model1 = get_embeddings_model()
    model2 = get_embeddings_model()
    assert model1 is model2


def test_embeddings_model_fallback_selected_on_dummy_key(monkeypatch):
    """Verify fallback path is taken when GEMINI_API_KEY starts with 'dummy' in non-production environment."""
    get_embeddings_model.cache_clear()
    monkeypatch.setattr(embeddings_module.settings, "ENVIRONMENT", "development")
    monkeypatch.setattr(embeddings_module.settings, "GEMINI_API_KEY", "dummy_key")

    model = get_embeddings_model()
    assert isinstance(model, _StubHuggingFaceEmbeddings)
    get_embeddings_model.cache_clear()


def test_embeddings_model_remote_selected_on_valid_key(monkeypatch):
    """Verify GoogleGenerativeAIEmbeddings is selected when a real API key is present."""
    get_embeddings_model.cache_clear()
    monkeypatch.setattr(embeddings_module.settings, "GEMINI_API_KEY", "valid_production_api_key_12345")

    model = get_embeddings_model()
    assert isinstance(model, _StubGoogleEmbeddings)
    assert model.model == "gemini-embedding-001"
    assert model.google_api_key == "valid_production_api_key_12345"
    get_embeddings_model.cache_clear()


def test_embeddings_model_production_missing_key_raises_runtime_error(monkeypatch):
    """Verify production fails fast when GEMINI_API_KEY is missing without loading HuggingFace/PyTorch."""
    get_embeddings_model.cache_clear()
    monkeypatch.setattr(embeddings_module.settings, "ENVIRONMENT", "production")
    monkeypatch.setattr(embeddings_module.settings, "GEMINI_API_KEY", "")

    with pytest.raises(RuntimeError) as exc_info:
        get_embeddings_model()

    assert "GEMINI_API_KEY must be configured" in str(exc_info.value)
    get_embeddings_model.cache_clear()


def test_embeddings_model_remote_failure_raises_runtime_error(monkeypatch):
    """Verify remote embedding failure raises RuntimeError without falling back to PyTorch/HF."""
    get_embeddings_model.cache_clear()
    monkeypatch.setattr(embeddings_module.settings, "ENVIRONMENT", "development")
    monkeypatch.setattr(embeddings_module.settings, "GEMINI_API_KEY", "valid_production_api_key_12345")

    def _failing_init(*args, **kwargs):
        raise ValueError("API Key invalid or quota exceeded for valid_production_api_key_12345")

    import langchain_google_genai
    monkeypatch.setattr(langchain_google_genai, "GoogleGenerativeAIEmbeddings", _failing_init)

    with pytest.raises(RuntimeError) as exc_info:
        get_embeddings_model()

    assert "Failed to initialize remote GoogleGenerativeAIEmbeddings" in str(exc_info.value)
    assert "valid_production_api_key_12345" not in str(exc_info.value)  # API key redacted
    get_embeddings_model.cache_clear()


def test_faiss_incompatible_model_identity_preserves_index(tmp_path, monkeypatch):
    """Verify FAISS index is not deleted on model identity mismatch, and descriptive ValueError is raised."""
    from langchain_community.vectorstores import FAISS

    # Restore real VectorStoreManager.add_documents for this test
    real_add_docs = _ORIGINAL_ADD_DOCUMENTS.__get__(None, VectorStoreManager)
    monkeypatch.setattr(VectorStoreManager, "add_documents", real_add_docs)

    monkeypatch.setattr(embeddings_module.settings, "VECTOR_STORE_DIR", str(tmp_path))
    user_id = "test_user_model_mismatch"
    index_path = VectorStoreManager._get_user_index_path(user_id)
    os.makedirs(index_path, exist_ok=True)

    # Create index with stub HF (model_name: stub-hf, dim: 384)
    stub_hf = _StubHuggingFaceEmbeddings()
    docs = [LCDocument(page_content="hello", metadata={"document_id": "1"})]
    vs = FAISS.from_documents(docs, stub_hf)
    vs.save_local(index_path)
    _save_index_metadata(index_path, "stub-hf", 384)

    # Attempt add_documents with stub Google (model: gemini-embedding-001, dim: 768)
    stub_google = _StubGoogleEmbeddings()
    import app.rag.vector_store as vector_store_module
    monkeypatch.setattr(vector_store_module, "get_embeddings_model", lambda: stub_google)

    with pytest.raises(ValueError) as exc_info:
        VectorStoreManager.add_documents(user_id, [LCDocument(page_content="new doc")])

    assert "FAISS index model identity/dimension mismatch" in str(exc_info.value)
    assert os.path.exists(os.path.join(index_path, "index.faiss"))  # Index is retained!
    assert os.path.exists(os.path.join(index_path, "index_metadata.json"))  # Metadata preserved!


@pytest.mark.asyncio
async def test_process_document_background_failure_updates_status(tmp_path):
    """Verify that a processing failure sets status='failed' with an error_message."""
    user_id = str(uuid.uuid4())
    doc_id = str(uuid.uuid4())

    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    async with db_module.AsyncSessionLocal() as db:
        doc = Document(
            id=doc_id,
            user_id=user_id,
            filename="empty.txt",
            file_path=str(empty_file),
            file_type="txt",
            file_size=0,
            status="processing",
            stage="validating",
            page_count=0,
            chunk_count=0
        )
        db.add(doc)
        await db.commit()

    await DocumentService.process_document_background(
        doc_id=doc_id,
        user_id=user_id,
        file_path=str(empty_file),
        filename="empty.txt"
    )

    async with db_module.AsyncSessionLocal() as db:
        res = await db.execute(select(Document).where(Document.id == doc_id))
        updated_doc = res.scalars().first()
        assert updated_doc is not None
        assert updated_doc.status == "failed"
        assert updated_doc.stage == "failed"
        assert updated_doc.error_message is not None
        assert (
            "No readable text" in updated_doc.error_message
            or "failed" in updated_doc.error_message.lower()
        )


@pytest.mark.asyncio
async def test_process_document_background_success(tmp_path):
    """Verify successful processing sets status='processed' and stage='ready'."""
    user_id = str(uuid.uuid4())
    doc_id = str(uuid.uuid4())

    sample_file = tmp_path / "sample.txt"
    sample_file.write_text(
        "Enterprise Multi-Agent RAG System test document content for embedding pipeline."
    )

    async with db_module.AsyncSessionLocal() as db:
        doc = Document(
            id=doc_id,
            user_id=user_id,
            filename="sample.txt",
            file_path=str(sample_file),
            file_type="txt",
            file_size=len(sample_file.read_bytes()),
            status="processing",
            stage="validating",
            page_count=0,
            chunk_count=0
        )
        db.add(doc)
        await db.commit()

    await DocumentService.process_document_background(
        doc_id=doc_id,
        user_id=user_id,
        file_path=str(sample_file),
        filename="sample.txt"
    )

    async with db_module.AsyncSessionLocal() as db:
        res = await db.execute(select(Document).where(Document.id == doc_id))
        updated_doc = res.scalars().first()
        assert updated_doc is not None
        assert updated_doc.status == "processed"
        assert updated_doc.stage == "ready"
        assert updated_doc.chunk_count > 0
        assert updated_doc.error_message is None
