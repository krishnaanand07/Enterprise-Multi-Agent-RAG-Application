"""
Document Pydantic schemas.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Schema for document metadata in API responses."""
    id: uuid.UUID
    original_filename: str
    file_type: str
    file_size: int
    num_pages: Optional[int] = None
    num_chunks: int = 0
    status: str
    created_at: datetime
    metadata_json: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    message: str
    document: DocumentResponse
