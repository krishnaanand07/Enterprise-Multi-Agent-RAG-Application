import uuid
from typing import List, Tuple
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Conversation, Message
from app.schemas.chat import ConversationCreateRequest, MessageCreateRequest
from app.agents.graph import run_agent_workflow


class ChatService:
    @staticmethod
    async def create_conversation(db: AsyncSession, user_id: str, request: ConversationCreateRequest) -> Conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=request.title or "New Chat"
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    @staticmethod
    async def list_conversations(db: AsyncSession, user_id: str) -> List[Conversation]:
        result = await db.execute(
            select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_messages(db: AsyncSession, user_id: str, conversation_id: str) -> List[Message]:
        conv_res = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        if not conv_res.scalars().first():
            raise HTTPException(status_code=404, detail="Conversation not found.")

        res = await db.execute(
            select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        )
        return res.scalars().all()

    @staticmethod
    async def send_message(db: AsyncSession, user_id: str, request: MessageCreateRequest) -> Tuple[Message, Message]:
        conv_res = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id, Conversation.user_id == user_id)
        )
        conversation = conv_res.scalars().first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found.")

        # Save user message
        user_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            role="user",
            content=request.content
        )
        db.add(user_msg)

        if conversation.title == "New Chat":
            conversation.title = request.content[:30] + ("..." if len(request.content) > 30 else "")

        await db.commit()

        # Run multi-agent graph with document-scoped filter option
        agent_result = await run_agent_workflow(
            query=request.content,
            user_id=user_id,
            conversation_id=conversation.id,
            selected_document_id=request.selected_document_id
        )

        # Save assistant response
        assistant_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            role="assistant",
            content=agent_result.get("response", "No response generated."),
            agent_used=agent_result.get("agent_used", "General Agent"),
            sources_json=agent_result.get("sources", []),
            metrics_json=agent_result.get("metrics", {})
        )
        db.add(assistant_msg)
        await db.commit()

        await db.refresh(user_msg)
        await db.refresh(assistant_msg)

        return user_msg, assistant_msg

    @staticmethod
    async def delete_conversation(db: AsyncSession, user_id: str, conversation_id: str) -> bool:
        res = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        conversation = res.scalars().first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found.")

        await db.delete(conversation)
        await db.commit()
        return True
