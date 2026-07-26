"""
Chat and conversation Pydantic schemas.
"""

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[uuid.UUID] = None


class CitationSchema(BaseModel):
    """Schema for a document citation."""
    document_name: str
    page_number: Optional[int] = None
    chunk_text: str
    relevance_score: float


class ChatResponse(BaseModel):
    """Schema for a chat response."""
    message: str
    conversation_id: uuid.UUID
    citations: List[CitationSchema] = []
    chart_data: Optional[dict] = None
    agent_used: Optional[str] = None
    tokens_used: Optional[int] = None


class ConversationResponse(BaseModel):
    """Schema for conversation metadata."""
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}
