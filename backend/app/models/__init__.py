"""
Database models package.

Import all models here so Alembic can discover them
for automatic migration generation.
"""

from app.models.user import User
from app.models.document import Document
from app.models.chat import Conversation, Message

__all__ = ["User", "Document", "Conversation", "Message"]
