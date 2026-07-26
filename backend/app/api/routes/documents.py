"""Document API routes."""
import os
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentUploadResponse, DocumentResponse
from app.api.deps import get_current_user
from app.utils.file_handler import save_upload_file
from app.rag.document_processing.pipeline import pipeline

router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a document and trigger processing."""
    
    # 1. Save file to disk safely
    file_path = await save_upload_file(file, current_user.id)
    
    # 2. Create DB record
    db_doc = Document(
        filename=os.path.basename(file_path),
        original_filename=file.filename,
        file_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(file_path),
        file_path=file_path,
        owner_id=current_user.id,
        status="processing"
    )
    db.add(db_doc)
    await db.commit()
    await db.refresh(db_doc)
    
    # 3. Trigger background processing (Extraction & Chunking)
    background_tasks.add_task(pipeline.process_document, db, db_doc)
    
    return {
        "message": "Document uploaded successfully and is being processed.",
        "document": db_doc
    }

@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all documents for the current user."""
    result = await db.execute(
        select(Document).where(Document.owner_id == current_user.id).order_by(Document.created_at.desc())
    )
    return list(result.scalars().all())
