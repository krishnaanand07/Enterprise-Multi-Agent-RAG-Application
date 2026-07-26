"""Chat API routes."""
import json
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.database.session import get_db
from app.models.user import User
from app.models.chat import Conversation, Message
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse
from app.api.deps import get_current_user
from app.agents.supervisor import supervisor

router = APIRouter()

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    title: str = "New Conversation",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new chat conversation."""
    conv = Conversation(title=title, user_id=current_user.id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all conversations for the current user."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
    )
    return list(result.scalars().all())

@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all messages for a specific conversation."""
    # Verify ownership
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return list(messages_result.scalars().all())

@router.post("/generate", response_model=ChatResponse)
async def generate_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to the AI agent and get a response.
    If conversation_id is not provided, a new one is created.
    """
    conversation_id = request.conversation_id
    
    # Create conversation if it doesn't exist
    if not conversation_id:
        conv = Conversation(title=request.message[:50] + "...", user_id=current_user.id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conversation_id = conv.id
    else:
        # Verify ownership
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Conversation not found")

    # Save User Message
    user_msg = Message(
        role="user",
        content=request.message,
        conversation_id=conversation_id
    )
    db.add(user_msg)
    await db.commit()

    # Call LangGraph Supervisor Agent
    try:
        agent_result = await supervisor.process_query(request.message, str(current_user.id))
        
        answer_text = agent_result.get("answer", "I could not generate an answer.")
        agent_used = agent_result.get("agent_used", "UNKNOWN")
        citations = agent_result.get("citations", [])
        chart_data = agent_result.get("chart_data", None)
        
        # Save AI Message with optional chart artifact
        ai_msg = Message(
            role="assistant",
            content=answer_text,
            conversation_id=conversation_id,
            agent_used=agent_used,
            citations=citations,
            chart_data=chart_data
        )
        db.add(ai_msg)
        await db.commit()
        
        return ChatResponse(
            message=answer_text,
            conversation_id=conversation_id,
            citations=citations,
            chart_data=chart_data,
            agent_used=agent_used
        )
        
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail="Error generating response from AI Agent.")
