import pytest
from app.rag.chunker import DocumentChunker

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
