from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    stage: str = "uploading"
    error_message: str | None = None
    page_count: int = 0
    chunk_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
