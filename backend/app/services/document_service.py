import os
import uuid
import shutil
import asyncio
import logging
import pandas as pd
from typing import List, Optional
from fastapi import UploadFile, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
import app.database.database as db_module
from app.models import Document, DocumentChunk, Dataset
from app.rag.loaders import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import VectorStoreManager

logger = logging.getLogger("enterprise_rag")


class DocumentService:
    @staticmethod
    async def upload_and_process(
        db: AsyncSession,
        user_id: str,
        file: UploadFile,
        background_tasks: Optional[BackgroundTasks] = None
    ) -> Document:
        ext = os.path.splitext(file.filename)[1].lower()
        allowed_exts = [".pdf", ".docx", ".txt", ".md", ".csv"]
        if ext not in allowed_exts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(allowed_exts)}"
            )

        user_upload_dir = os.path.join(settings.UPLOAD_DIR, f"user_{user_id}")
        os.makedirs(user_upload_dir, exist_ok=True)

        doc_id = str(uuid.uuid4())
        file_path = os.path.join(user_upload_dir, f"{doc_id}_{file.filename}")

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_size = os.path.getsize(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

        document = Document(
            id=doc_id,
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            file_type=ext.replace(".", ""),
            file_size=file_size,
            status="processing",
            stage="validating",
            page_count=0,
            chunk_count=0
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)

        if background_tasks is not None:
            background_tasks.add_task(
                DocumentService.process_document_background,
                doc_id=doc_id,
                user_id=user_id,
                file_path=file_path,
                filename=file.filename
            )
        else:
            # Inline processing for unit tests or environments without BackgroundTasks
            await DocumentService.process_document_background(
                doc_id=doc_id,
                user_id=user_id,
                file_path=file_path,
                filename=file.filename
            )
            # Re-fetch updated document state
            result = await db.execute(select(Document).where(Document.id == doc_id))
            document = result.scalars().first()

        return document

    @staticmethod
    async def process_document_background(
        doc_id: str,
        user_id: str,
        file_path: str,
        filename: str
    ):
        """Asynchronous background worker executing stages with offloaded CPU embedding computation."""
        ext = os.path.splitext(filename)[1].lower()

        async with db_module.AsyncSessionLocal() as db:
            result = await db.execute(select(Document).where(Document.id == doc_id))
            doc = result.scalars().first()
            if not doc:
                return

            try:
                logger.info(f"Starting background processing for document '{filename}' (ID: {doc_id})")
                # Stage 1: Extracting text
                doc.stage = "extracting"
                await db.commit()

                pages, file_type = await asyncio.to_thread(
                    DocumentLoader.load_file, file_path, filename
                )
                doc.page_count = len(pages)
                doc.stage = "chunking"
                await db.commit()

                # Stage 2: Chunking document
                chunker = DocumentChunker()
                lc_chunks = await asyncio.to_thread(
                    chunker.chunk_document, pages, doc_id, filename, user_id
                )

                if not lc_chunks:
                    raise ValueError("No readable text content could be extracted from document.")

                # Stage 3: Generating embeddings & Updating Vector Store
                logger.info(f"Embedding start: Beginning embedding generation for document '{filename}' ({len(lc_chunks)} chunks)...")
                doc.stage = "embedding"
                await db.commit()

                success = await asyncio.to_thread(
                    VectorStoreManager.add_documents,
                    user_id=user_id,
                    documents=lc_chunks
                )

                if not success:
                    raise RuntimeError("Failed to index document chunks into vector store.")

                logger.info(f"Embedding completion: Vectors successfully generated and saved for document '{filename}'.")
                doc.stage = "indexing"
                await db.commit()

                # Stage 4: Database chunk records & dataset metadata
                for idx, lc_chunk in enumerate(lc_chunks):
                    chunk_record = DocumentChunk(
                        id=str(uuid.uuid4()),
                        document_id=doc_id,
                        chunk_index=idx + 1,
                        content=lc_chunk.page_content,
                        metadata_json=lc_chunk.metadata
                    )
                    db.add(chunk_record)

                if ext == ".csv":
                    df = pd.read_csv(file_path)
                    table_name = f"dataset_{doc_id.replace('-', '_')}"
                    schema_info = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}

                    dataset_record = Dataset(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        document_id=doc_id,
                        table_name=table_name,
                        schema_info=schema_info,
                        row_count=len(df)
                    )
                    db.add(dataset_record)

                # Final Stage: Ready
                doc.status = "processed"
                doc.stage = "ready"
                doc.chunk_count = len(lc_chunks)
                doc.error_message = None
                await db.commit()
                logger.info(f"Final document status: Document processing completed successfully for '{filename}' ({len(lc_chunks)} chunks, status='processed', stage='ready').")

            except Exception as e:
                logger.error(f"Error processing document '{filename}' (ID: {doc_id}): {str(e)}", exc_info=True)
                try:
                    await db.rollback()
                    res = await db.execute(select(Document).where(Document.id == doc_id))
                    doc_err = res.scalars().first()
                    if doc_err:
                        doc_err.status = "failed"
                        doc_err.stage = "failed"
                        doc_err.error_message = str(e)
                        await db.commit()
                        logger.info(f"Final document status: Updated document '{filename}' (ID: {doc_id}) to status='failed', stage='failed', error='{str(e)}'")
                except Exception as db_err:
                    logger.error(f"Failed to update document '{filename}' status to failed: {str(db_err)}")

    @staticmethod
    async def list_user_documents(db: AsyncSession, user_id: str) -> List[Document]:
        result = await db.execute(
            select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_document_by_id(db: AsyncSession, user_id: str, document_id: str) -> Document:
        result = await db.execute(
            select(Document).where(Document.id == document_id, Document.user_id == user_id)
        )
        doc = result.scalars().first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        return doc

    @staticmethod
    async def delete_document(db: AsyncSession, user_id: str, document_id: str) -> bool:
        result = await db.execute(
            select(Document).where(Document.id == document_id, Document.user_id == user_id)
        )
        document = result.scalars().first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")

        VectorStoreManager.delete_document(user_id, document_id)

        if os.path.exists(document.file_path):
            try:
                os.remove(document.file_path)
            except Exception:
                pass

        await db.delete(document)
        await db.commit()
        return True
