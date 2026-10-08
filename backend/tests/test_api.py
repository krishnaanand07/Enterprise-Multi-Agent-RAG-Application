"""
API Integration Tests for FastAPI Backend.
Run with: pytest tests/
"""
import os
import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.database import Base, get_db
import app.database.database as db_module
import app.models  # Ensures all ORM models register on Base.metadata
from app.main import app
from app.core.config import settings

settings.ENVIRONMENT = "testing"
settings.GEMINI_API_KEY = "dummy_test_key_for_unit_tests"

TEST_DB_FILE = os.path.join(os.path.dirname(__file__), "test_api_app_db.sqlite")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

override_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)
override_session_factory = async_sessionmaker(bind=override_engine, class_=AsyncSession, expire_on_commit=False)

db_module.engine = override_engine
db_module.AsyncSessionLocal = override_session_factory

async def _override_get_db():
    async with override_session_factory() as session:
        yield session

app.dependency_overrides[get_db] = _override_get_db

@pytest.fixture(autouse=True)
async def setup_test_schema():
    """Initializes schema in SQLite database for test execution."""
    async with override_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with override_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

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
        response = await ac.get("/api/v1/auth/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_registration_login_and_auth_flow():
    """Test registration with valid data, duplicate email check, login, and authenticated endpoint retrieval."""
    unique_str = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_str}@example.com"
    test_password = "password123"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register valid user
        reg_payload = {
            "email": test_email,
            "password": test_password,
            "full_name": "Test User"
        }
        reg_response = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert reg_response.status_code == 201, reg_response.text
        reg_data = reg_response.json()
        assert reg_data["email"] == test_email

        # 2. Duplicate registration attempt (expect 409 Conflict)
        dup_response = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert dup_response.status_code == 409
        assert "already exists" in dup_response.json()["detail"]

        # 3. Login with registered credentials
        login_data = {
            "email": test_email,
            "password": test_password
        }
        login_response = await ac.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        token = token_data["access_token"]

        # 4. Authenticated request using JWT Bearer token
        auth_headers = {"Authorization": f"Bearer {token}"}
        me_response = await ac.get("/api/v1/auth/me", headers=auth_headers)
        assert me_response.status_code == 200
        user_profile = me_response.json()
        assert user_profile["email"] == test_email
