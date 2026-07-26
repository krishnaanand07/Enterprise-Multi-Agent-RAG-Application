"""
Document database model.

Stores metadata about uploaded documents.
The actual file content is stored on disk (uploads/ directory).
Chunks and embeddings are stored in the vector database.
"""

import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    filename: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    original_filename: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    file_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    file_size: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    file_path: Mapped[str] = mapped_column(
        String(1000), nullable=False
    )
    num_pages: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    num_chunks: Mapped[int] = mapped_column(
        Integer, default=0
    )
    status: Mapped[str] = mapped_column(
        String(50), default="processing"
    )
    metadata_json: Mapped[dict] = mapped_column(
        JSONB, default=dict, nullable=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename={self.original_filename})>"
