"""
Orchestrates the document ingestion pipeline.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models.document import Document
from app.rag.document_processing.extractor import extractor
from app.rag.document_processing.chunker import chunker

class DocumentPipeline:
    async def process_document(self, db: AsyncSession, document: Document):
        """Run the end-to-end extraction and chunking pipeline."""
        try:
            logger.info(f"Starting processing for document {document.id}")
            
            # 1. Extract text
            text, metadata = extractor.extract_text(document.file_path)
            
            # 2. Chunk text
            chunks = chunker.chunk_text(text)
            
            # 3. Create Metadatas and Store in Vector DB
            if chunks:
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
            
            # 4. Update Database Record
            document.status = "processed"
            document.num_pages = metadata.get("num_pages")
            document.num_chunks = len(chunks)
            
            db.add(document)
            await db.commit()
            logger.info(f"Successfully processed document {document.id} into {len(chunks)} chunks.")
            
        except Exception as e:
            logger.error(f"Failed to process document {document.id}: {e}")
            document.status = "failed"
            db.add(document)
            await db.commit()

pipeline = DocumentPipeline()
