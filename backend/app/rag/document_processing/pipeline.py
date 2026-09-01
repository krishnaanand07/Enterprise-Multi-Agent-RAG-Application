"""
Orchestrates the document ingestion pipeline.

Key improvements:
  - All blocking calls (extract, chunk, embed) run in asyncio.to_thread()
    so the event loop is never stalled.
  - Per-stage timeouts prevent any single stage from hanging forever.
  - Detailed status updates + error reason stored for debugging.
"""
import asyncio
import uuid
from sqlalchemy import select
from loguru import logger

from app.database.session import async_session_factory
from app.models.document import Document
from app.rag.document_processing.extractor import extractor
from app.rag.document_processing.chunker import chunker

# Per-stage timeout constants (seconds)
EXTRACT_TIMEOUT = 120   # up to 2 min for large PDFs / big PPTXes
CHUNK_TIMEOUT   = 60    # chunking should always be fast
EMBED_TIMEOUT   = 300   # embedding can be slow for many chunks (API rate limits)


class DocumentPipeline:

    async def process_document_by_id(self, document_id: str):
        """
        Run the end-to-end extraction → chunking → embedding pipeline.
        Uses an isolated DB session and wraps every blocking call in a
        thread pool so the FastAPI event loop stays responsive.
        """
        doc_uuid = uuid.UUID(document_id) if isinstance(document_id, str) else document_id

        async with async_session_factory() as db:
            try:
                result = await db.execute(select(Document).where(Document.id == doc_uuid))
                document = result.scalar_one_or_none()
                if not document:
                    logger.error(
                        f"Document {document_id} not found in DB for background processing."
                    )
                    return

                logger.info(
                    f"▶ Starting pipeline for doc {document_id} "
                    f"({document.original_filename})"
                )

                # ── Stage 1: Extract ─────────────────────────────────────
                document.status = "extracting"
                db.add(document)
                await db.commit()

                try:
                    text, metadata = await asyncio.wait_for(
                        extractor.extract_text_async(document.file_path),
                        timeout=EXTRACT_TIMEOUT,
                    )
                except asyncio.TimeoutError:
                    raise RuntimeError(
                        f"Text extraction timed out after {EXTRACT_TIMEOUT}s "
                        f"for file: {document.original_filename}"
                    )

                logger.info(
                    f"✔ Extracted {len(text):,} chars from {document.original_filename}"
                )

                # ── Stage 2: Chunk ───────────────────────────────────────
                document.status = "chunking"
                db.add(document)
                await db.commit()

                try:
                    chunks: list[str] = await asyncio.wait_for(
                        asyncio.to_thread(chunker.chunk_text, text),
                        timeout=CHUNK_TIMEOUT,
                    )
                except asyncio.TimeoutError:
                    raise RuntimeError(
                        f"Text chunking timed out after {CHUNK_TIMEOUT}s"
                    )

                logger.info(
                    f"✔ Created {len(chunks)} chunks from {document.original_filename}"
                )

                # ── Stage 3: Embed & store ───────────────────────────────
                if chunks:
                    document.status = "embedding"
                    db.add(document)
                    await db.commit()

                    from app.rag.vector_db.faiss_store import faiss_store

                    metadatas = [
                        {
                            "document_id": str(document.id),
                            "filename": document.original_filename,
                            "chunk_index": i,
                        }
                        for i in range(len(chunks))
                    ]

                    try:
                        await asyncio.wait_for(
                            faiss_store.add_texts_async(
                                texts=chunks,
                                metadatas=metadatas,
                                namespace=str(document.owner_id),
                            ),
                            timeout=EMBED_TIMEOUT,
                        )
                    except asyncio.TimeoutError:
                        raise RuntimeError(
                            f"Embedding timed out after {EMBED_TIMEOUT}s "
                            f"({len(chunks)} chunks). Try a smaller document."
                        )

                    logger.info(
                        f"✔ Embedded {len(chunks)} chunks for {document.original_filename}"
                    )
                else:
                    logger.warning(
                        f"No chunks produced for {document.original_filename} — "
                        "file may be empty or image-only."
                    )

                # ── Stage 4: Mark processed ──────────────────────────────
                document.status = "processed"
                document.num_pages = metadata.get("num_pages", 1)
                document.num_chunks = len(chunks)
                db.add(document)
                await db.commit()

                logger.info(
                    f"✅ Done: doc {document.id} → "
                    f"{len(chunks)} chunks, {document.num_pages} pages"
                )

            except Exception as exc:
                logger.error(f"❌ Pipeline failed for doc {document_id}: {exc}")
                try:
                    result = await db.execute(
                        select(Document).where(Document.id == doc_uuid)
                    )
                    document = result.scalar_one_or_none()
                    if document:
                        document.status = "failed"
                        db.add(document)
                        await db.commit()
                except Exception as inner:
                    logger.error(
                        f"Could not set status=failed for doc {document_id}: {inner}"
                    )

    async def process_document(self, db, document):
        """Backward-compatible entry point."""
        await self.process_document_by_id(str(document.id))


pipeline = DocumentPipeline()
