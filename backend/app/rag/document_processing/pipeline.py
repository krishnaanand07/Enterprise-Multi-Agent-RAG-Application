"""
Orchestrates the document ingestion pipeline.
"""
import uuid
from sqlalchemy import select
from loguru import logger

from app.database.session import async_session_factory
from app.models.document import Document
from app.rag.document_processing.extractor import extractor
from app.rag.document_processing.chunker import chunker


class DocumentPipeline:
    async def process_document_by_id(self, document_id: str):
        """Run the end-to-end extraction, chunking, and embedding pipeline using an isolated DB session."""
        doc_uuid = uuid.UUID(document_id) if isinstance(document_id, str) else document_id

        async with async_session_factory() as db:
            try:
                result = await db.execute(select(Document).where(Document.id == doc_uuid))
                document = result.scalar_one_or_none()
                if not document:
                    logger.error(f"Document {document_id} not found in database for background processing.")
                    return

                logger.info(f"Starting background processing for document {document_id} ({document.original_filename})")

                # 1. Extract text
                document.status = "extracting"
                db.add(document)
                await db.commit()

                text, metadata = extractor.extract_text(document.file_path)

                # 2. Chunk text
                document.status = "chunking"
                db.add(document)
                await db.commit()

                chunks = chunker.chunk_text(text)

                # 3. Create Metadatas and Store in Vector DB
                if chunks:
                    document.status = "embedding"
                    db.add(document)
                    await db.commit()

                    from app.rag.vector_db.faiss_store import faiss_store
                    metadatas = [
                        {
                            "document_id": str(document.id),
                            "filename": document.original_filename,
                            "chunk_index": i
                        }
                        for i in range(len(chunks))
                    ]
                    faiss_store.add_texts(
                        texts=chunks,
                        metadatas=metadatas,
                        namespace=str(document.owner_id)
                    )

                # 4. Update Database Record to Processed
                document.status = "processed"
                document.num_pages = metadata.get("num_pages", 1)
                document.num_chunks = len(chunks)

                db.add(document)
                await db.commit()
                logger.info(f"Successfully processed document {document.id} into {len(chunks)} chunks.")

            except Exception as e:
                logger.error(f"Failed to process document {document_id}: {e}")
                try:
                    result = await db.execute(select(Document).where(Document.id == doc_uuid))
                    document = result.scalar_one_or_none()
                    if document:
                        document.status = "failed"
                        db.add(document)
                        await db.commit()
                except Exception as inner_e:
                    logger.error(f"Failed to set status to failed for document {document_id}: {inner_e}")

    async def process_document(self, db, document):
        """Backward compatible entrypoint."""
        await self.process_document_by_id(str(document.id))


pipeline = DocumentPipeline()
