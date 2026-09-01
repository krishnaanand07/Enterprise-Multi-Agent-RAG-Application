"""
Utility for safely saving and validating uploaded files.
Supports: PDF, DOCX, PPTX, TXT, MD, CSV, XLSX
"""
import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile, HTTPException

from app.config.settings import settings

# Expanded list — now includes PPTX, XLSX, MD
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx", ".pptx", ".csv", ".xlsx"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
CHUNK_READ_SIZE = 1024 * 1024  # 1 MB read chunks


async def save_upload_file(upload_file: UploadFile, user_id: uuid.UUID) -> str:
    """
    Validates and saves an uploaded file to disk asynchronously.
    Returns the saved file path as a string.
    """
    filename = upload_file.filename or ""
    ext = Path(filename).suffix.lower()

    if not ext or ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext or 'none'}'. "
                   f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    upload_dir = Path("uploads") / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = upload_dir / unique_filename

    size = 0
    try:
        # Use aiofiles for non-blocking disk I/O
        async with aiofiles.open(file_path, "wb") as buffer:
            while True:
                chunk = await upload_file.read(CHUNK_READ_SIZE)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)} MB.",
                    )
                await buffer.write(chunk)
    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}") from e

    return str(file_path)
