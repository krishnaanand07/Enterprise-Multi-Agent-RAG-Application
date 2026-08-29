"""
API Integration Tests for FastAPI Backend.
Run with: pytest tests/
"""
import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.config.settings import settings
settings.ENVIRONMENT = "testing"

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models import user, document, chat  # Ensures all models register with Base.metadata

import os
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_api.db")

# ── Isolated Test Database ─────────────────────────────────────
test_engine = create_async_engine(
    f"sqlite+aiosqlite:///{TEST_DB_PATH}",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
test_async_session = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


async def _override_get_db():
    """Overrides the default database dependency for API test routes."""
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True, scope="module")
async def setup_test_schema():
    """Initializes schema in SQLite database once for the test module."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_root_health_check():
    """Test the primary lightweight /health endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_api_health_check():
    """Test the /api/health endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test that protected routes require a valid Bearer token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_cors_options_preflight():
    """Test OPTIONS preflight request handling for CORS."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        }
        response = await ac.options("/api/auth/register", headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
async def test_registration_login_and_auth_flow():
    """Test registration with valid data, duplicate email check, login, and authenticated endpoint retrieval."""
    unique_str = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_str}@example.com"
    test_username = f"user_{unique_str}"
    test_password = "password123"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register valid user
        reg_payload = {
            "email": test_email,
            "username": test_username,
            "password": test_password,
            "full_name": "Test User"
        }
        reg_response = await ac.post("/api/auth/register", json=reg_payload)
        assert reg_response.status_code == 201, reg_response.text
        reg_data = reg_response.json()
        assert reg_data["email"] == test_email
        assert reg_data["username"] == test_username

        # 2. Duplicate registration attempt (expect 400 Bad Request)
        dup_response = await ac.post("/api/auth/register", json=reg_payload)
        assert dup_response.status_code == 400
        assert "Email already registered" in dup_response.json()["detail"]

        # 3. Login with registered credentials
        login_data = {
            "username": test_email,
            "password": test_password
        }
        login_response = await ac.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        token = token_data["access_token"]

        # 4. Authenticated request using JWT Bearer token
        auth_headers = {"Authorization": f"Bearer {token}"}
        me_response = await ac.get("/api/users/me", headers=auth_headers)
        assert me_response.status_code == 200
        user_profile = me_response.json()
        assert user_profile["email"] == test_email


@pytest.mark.asyncio
async def test_public_auth_routes_ignore_extraneous_auth_headers():
    """Test that public endpoints (/auth/register and /auth/login) process requests properly regardless of stale auth headers."""
    unique_str = str(uuid.uuid4())[:8]
    test_email = f"stale_{unique_str}@example.com"
    test_username = f"stale_{unique_str}"
    test_password = "password123"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": "Bearer STALE_EXPIRED_TOKEN_EXAMPLE"}
        reg_payload = {
            "email": test_email,
            "username": test_username,
            "password": test_password,
            "full_name": "Stale Token User"
        }
        reg_response = await ac.post("/api/auth/register", json=reg_payload, headers=headers)
        assert reg_response.status_code == 201
