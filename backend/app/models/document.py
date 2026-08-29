"""
Document database model.

Stores metadata about uploaded documents.
The actual file content is stored on disk (uploads/ directory).
Chunks and embeddings are stored in the vector database.
"""

import uuid
from sqlalchemy import String, Integer, ForeignKey, JSON, Uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin

UUID_TYPE = UUID(as_uuid=True).with_variant(Uuid(as_uuid=True), "sqlite")
JSON_TYPE = JSONB().with_variant(JSON(), "sqlite")


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
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
        JSON_TYPE, default=dict, nullable=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID_TYPE,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename={self.original_filename})>"
