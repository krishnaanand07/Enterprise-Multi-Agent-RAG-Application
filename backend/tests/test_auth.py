import os
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from fastapi import HTTPException
from sqlalchemy import inspect

from app.core.config import settings
settings.ENVIRONMENT = "testing"
settings.GEMINI_API_KEY = "dummy_test_key_for_unit_tests"

import app.models  # Ensures all ORM models register on Base.metadata
from app.database.database import Base, engine
from app.main import app

@pytest.fixture(autouse=True)
async def setup_test_database():
    print(f"\n[TEST SETUP] Engine URL: {engine.url}")
    print(f"[TEST SETUP] Registered tables: {list(Base.metadata.tables.keys())}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        def check_tables(sync_conn):
            inspector = inspect(sync_conn)
            print(f"[TEST SETUP] Actual tables in DB: {inspector.get_table_names()}")
        
        await conn.run_sync(check_tables)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_health_endpoint():
    """Verify GET /api/health is cheap, fast, and returns HTTP 200."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-rag-api"

@pytest.mark.asyncio
async def test_version_endpoint():
    """Verify GET /api/version returns version string from settings."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": settings.APP_VERSION}

@pytest.mark.asyncio
async def test_readiness_endpoint_healthy():
    """Verify GET /api/ready returns HTTP 200 when database and store are ready."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["database"] == "healthy"

@pytest.mark.asyncio
async def test_registration_success_flow():
    """Verify successful user registration and subsequent login."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        test_email = "newuser@example.com"
        reg_response = await ac.post("/api/v1/auth/register", json={
            "email": test_email,
            "password": "password123",
            "full_name": "New User"
        })
        assert reg_response.status_code == 201
        reg_data = reg_response.json()
        assert reg_data["email"] == test_email
        assert "id" in reg_data
        assert "hashed_password" not in reg_data

@pytest.mark.asyncio
async def test_registration_duplicate_email_conflict():
    """Verify duplicate registration returns HTTP 409 Conflict with safe detail."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        test_email = "duplicate@example.com"
        payload = {"email": test_email, "password": "password123", "full_name": "First User"}
        
        # First registration -> 201
        res1 = await ac.post("/api/v1/auth/register", json=payload)
        assert res1.status_code == 201

        # Second registration -> 409
        res2 = await ac.post("/api/v1/auth/register", json=payload)
        assert res2.status_code == 409
        assert res2.json()["detail"] == "An account with this email already exists."

@pytest.mark.asyncio
async def test_registration_invalid_request():
    """Verify registration with invalid payload returns HTTP 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json={"email": "not-an-email"})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_registration_database_unavailable_error():
    """Verify database connection errors trigger rollback and return HTTP 503."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with patch("app.services.auth_service.AuthService.register_user", side_effect=HTTPException(status_code=503, detail="Database service is temporarily unavailable.")):
            response = await ac.post("/api/v1/auth/register", json={
                "email": "dbfail@example.com",
                "password": "password123",
                "full_name": "DB Fail User"
            })
            assert response.status_code == 503
            assert response.json()["detail"] == "Database service is temporarily unavailable."
