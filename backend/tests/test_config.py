import os
import pytest
from app.core.config import Settings
from app.main import app


def test_allowed_origins_default(monkeypatch):
    monkeypatch.delenv("ALLOWED_ORIGINS", raising=False)
    settings = Settings()
    assert isinstance(settings.ALLOWED_ORIGINS, list)
    assert "http://localhost:8000" in settings.ALLOWED_ORIGINS
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS


def test_allowed_origins_json_env(monkeypatch):
    env_val = '["http://localhost:3000", "https://example.vercel.app"]'
    monkeypatch.setenv("ALLOWED_ORIGINS", env_val)
    settings = Settings()
    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:3000",
        "https://example.vercel.app",
    ]


def test_allowed_origins_comma_separated_env(monkeypatch):
    env_val = "http://localhost:3000, https://example.vercel.app"
    monkeypatch.setenv("ALLOWED_ORIGINS", env_val)
    settings = Settings()
    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:3000",
        "https://example.vercel.app",
    ]


def test_allowed_origins_single_url_env(monkeypatch):
    env_val = "https://example.vercel.app"
    monkeypatch.setenv("ALLOWED_ORIGINS", env_val)
    settings = Settings()
    assert settings.ALLOWED_ORIGINS == ["https://example.vercel.app"]


def test_allowed_origins_empty_env(monkeypatch):
    monkeypatch.setenv("ALLOWED_ORIGINS", "  ")
    settings = Settings()
    assert settings.ALLOWED_ORIGINS == []


def test_fastapi_app_imports_and_cors_initialized():
    assert app.title == "Enterprise RAG Assistant"
    # Find CORSMiddleware in middleware stack
    cors_middleware = [
        m for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware"
    ]
    assert len(cors_middleware) == 1
    assert "allow_origins" in cors_middleware[0].kwargs
    assert isinstance(cors_middleware[0].kwargs["allow_origins"], list)

