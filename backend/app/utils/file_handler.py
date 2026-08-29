"""
Utility for safely saving and validating uploaded files.
"""
import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.config.settings import settings

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

async def save_upload_file(upload_file: UploadFile, user_id: uuid.UUID) -> str:
    """Validates and saves an uploaded file to the local disk."""
    filename = upload_file.filename or ""
    ext = Path(filename).suffix.lower()
    if not ext or ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext or 'none'}")
        
    upload_dir = Path("uploads") / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = upload_dir / unique_filename
    
    # Read in chunks to avoid memory issues with large files
    size = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := await upload_file.read(1024 * 1024):  # 1MB chunks
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File too large")
                buffer.write(chunk)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise e
    finally:
        await upload_file.seek(0)
        
    return str(file_path)
