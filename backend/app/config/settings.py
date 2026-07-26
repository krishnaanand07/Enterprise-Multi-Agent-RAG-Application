"""
Application configuration using Pydantic BaseSettings.

All environment variables are validated at startup. If a required
variable is missing, the application fails immediately with a
clear error message rather than failing at runtime.
"""

from pathlib import Path
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """
    Central configuration for the application.
    Values are loaded from environment variables or .env file.
    """

    # ── Application ──────────────────────────────────────────
    APP_NAME: str = "Enterprise RAG Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-me-in-production"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # ── Database ─────────────────────────────────────────────
    POSTGRES_USER: str = "rag_user"
    POSTGRES_PASSWORD: str = "rag_password_change_me"
    POSTGRES_DB: str = "rag_assistant"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = (
        "postgresql+asyncpg://rag_user:rag_password_change_me"
        "@localhost:5432/rag_assistant"
    )

    # ── JWT ──────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── LLM ──────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    NVIDIA_API_KEY: str = ""
    NVIDIA_MODEL: str = "meta/llama-3.1-8b-instruct"
    LLM_PROVIDER: str = "gemini"  # "gemini", "openai", or "nvidia"

    # ── Embeddings ───────────────────────────────────────────
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # ── Vector Database ──────────────────────────────────────
    VECTOR_DB_PROVIDER: str = "faiss"  # "faiss" or "chroma"
    FAISS_INDEX_PATH: str = "./vector_db/faiss_index"
    CHROMA_PERSIST_DIR: str = "./vector_db/chroma_db"
    CHROMA_COLLECTION_NAME: str = "rag_documents"

    # ── Document Processing ──────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".docx", ".txt", ".csv",
        ".png", ".jpg", ".jpeg",
    ]
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # ── Web Search ───────────────────────────────────────────
    TAVILY_API_KEY: str = ""

    # ── Logging ──────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


# Singleton instance — import this everywhere
settings = Settings()
