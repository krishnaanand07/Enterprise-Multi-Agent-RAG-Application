from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ConversationCreateRequest(BaseModel):
    title: Optional[str] = "New Chat"


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreateRequest(BaseModel):
    conversation_id: str
    content: str
    selected_document_id: Optional[str] = None   # Document-Scoped Chat filter option


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    agent_used: Optional[str] = None
    sources_json: Optional[List[Dict[str, Any]]] = None
    metrics_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
