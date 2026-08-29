"""
Chat and conversation database models.

Conversations group related messages together.
Each message stores the role (user/assistant), content,
and optional citations from document retrieval.
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, Integer, JSON, Uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

UUID_TYPE = UUID(as_uuid=True).with_variant(Uuid(as_uuid=True), "sqlite")
JSON_TYPE = JSONB().with_variant(JSON(), "sqlite")


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(500), default="New Conversation"
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title})>"


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
        primary_key=True,
        default=uuid.uuid4,
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    citations: Mapped[dict] = mapped_column(
        JSON_TYPE, default=list, nullable=True
    )
    chart_data: Mapped[dict] = mapped_column(
        JSON_TYPE, nullable=True
    )
    agent_used: Mapped[str] = mapped_column(
        String(50), nullable=True
    )
    tokens_used: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role})>"
