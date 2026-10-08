from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.chat import (
    ConversationCreateRequest,
    ConversationResponse,
    MessageCreateRequest,
    MessageResponse
)
from app.services.chat_service import ChatService
from app.api.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat conversation."""
    return await ChatService.create_conversation(db, current_user.id, request)


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all previous conversations for the authenticated user."""
    return await ChatService.list_conversations(db, current_user.id)


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all messages in a specific conversation."""
    return await ChatService.get_messages(db, current_user.id, conversation_id)


@router.post("/messages", response_model=List[MessageResponse])
async def send_message(
    request: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send user message, execute LangGraph agent, and return user + assistant messages."""
    user_msg, assistant_msg = await ChatService.send_message(db, current_user.id, request)
    return [user_msg, assistant_msg]


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation and all its messages."""
    await ChatService.delete_conversation(db, current_user.id, conversation_id)
    return None
