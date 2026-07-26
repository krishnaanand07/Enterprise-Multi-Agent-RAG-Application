"""
Basic API Tests for the FastAPI Backend.
Run with: pytest tests/test_api.py
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is running"}

@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test that protected routes require a token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
