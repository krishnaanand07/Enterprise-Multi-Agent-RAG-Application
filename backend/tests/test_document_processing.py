"""
Unit tests for Document Ingestion Pipeline, Embedding Model Caching, and Background Exception Handling.
"""
import os
import pytest
import uuid
from app.rag.embeddings import get_embeddings_model
from app.services.document_service import DocumentService
from app.models import Document
from app.database.database import Base
import app.database.database as db_module
from sqlalchemy.future import select


@pytest.fixture(autouse=True)
async def setup_test_schema():
    """Initializes schema in database for test execution."""
    async with db_module.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


def test_embeddings_model_caching():
    """Verify get_embeddings_model uses lru_cache singleton."""
    model1 = get_embeddings_model()
    model2 = get_embeddings_model()
    assert model1 is model2


@pytest.mark.asyncio
async def test_process_document_background_failure_updates_status(tmp_path):
    """Verify that an exception during document processing sets status to 'failed' with error_message."""
    user_id = str(uuid.uuid4())
    doc_id = str(uuid.uuid4())
    
    # Create empty file that yields 0 chunks
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

    # Process in background runner
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
        assert "No readable text" in updated_doc.error_message or "failed" in updated_doc.error_message.lower()


@pytest.mark.asyncio
async def test_process_document_background_success(tmp_path):
    """Verify successful background processing updates status to 'processed' and stage to 'ready'."""
    user_id = str(uuid.uuid4())
    doc_id = str(uuid.uuid4())
    
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Enterprise Multi-Agent RAG System test document content for embedding pipeline.")

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
