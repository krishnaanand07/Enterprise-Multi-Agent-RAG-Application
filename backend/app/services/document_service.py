import os
import uuid
import shutil
import pandas as pd
from typing import List
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.models import Document, DocumentChunk, Dataset
from app.rag.loaders import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import VectorStoreManager


class DocumentService:
    @staticmethod
    async def upload_and_process(db: AsyncSession, user_id: str, file: UploadFile) -> Document:
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
            status="processing"
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)

        try:
            pages, file_type = DocumentLoader.load_file(file_path, file.filename)
            chunker = DocumentChunker()
            lc_chunks = chunker.chunk_document(pages, doc_id, file.filename, user_id)

            for idx, lc_chunk in enumerate(lc_chunks):
                chunk_record = DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=doc_id,
                    chunk_index=idx + 1,
                    content=lc_chunk.page_content,
                    metadata_json=lc_chunk.metadata
                )
                db.add(chunk_record)

            VectorStoreManager.add_documents(user_id, lc_chunks)

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

            document.status = "processed"
            document.chunk_count = len(lc_chunks)
            await db.commit()
            await db.refresh(document)
            return document

        except Exception as e:
            document.status = "failed"
            await db.commit()
            raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

    @staticmethod
    async def list_user_documents(db: AsyncSession, user_id: str) -> List[Document]:
        result = await db.execute(
            select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        )
        return result.scalars().all()

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
