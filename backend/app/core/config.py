import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "Enterprise RAG Assistant"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Security & JWT
    SECRET_KEY: str = "super-secret-enterprise-rag-key-change-in-production"
    JWT_SECRET_KEY: str = "jwt-secret-enterprise-rag-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    # Gemini LLM Settings
    GEMINI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Embeddings Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    # File Storage & RAG Settings
    UPLOAD_DIR: str = "./uploads"
    VECTOR_STORE_DIR: str = "./vector_db/faiss_index"
    MAX_FILE_SIZE_MB: int = 50
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", "backend/.env", "backend/.env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("GEMINI_API_KEY", mode="before")
    @classmethod
    def resolve_gemini_key(cls, v: str) -> str:
        if v:
            return v
        return os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))


settings = Settings()
