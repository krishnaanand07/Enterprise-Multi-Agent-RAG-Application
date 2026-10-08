import os
from fastapi import APIRouter, Response, status
from app.core.config import settings
from app.database.database import check_database_health
from app.services.llm_service import llm_service

router = APIRouter(prefix="", tags=["Health & Monitoring"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Lightweight Liveness Endpoint.
    Fast & cheap check to confirm the FastAPI server process is responding.
    Does NOT query DB, Gemini, or FAISS. Suitable for external monitors (UptimeRobot).
    """
    return {
        "status": "healthy",
        "service": "enterprise-rag-api"
    }


@router.get("/version", status_code=status.HTTP_200_OK)
async def version_check():
    """Returns application version."""
    return {
        "version": settings.APP_VERSION
    }


@router.get("/ready")
async def readiness_check(response: Response):
    """
    Deep Readiness Endpoint.
    Verifies Database connectivity (SELECT 1), Vector Store state, and required Configuration.
    Returns HTTP 200 if ready, or HTTP 503 if a critical dependency is unavailable.
    Never exposes secrets or stack traces.
    """
    db_healthy = await check_database_health()
    
    # Check configuration
    has_db_url = bool(settings.DATABASE_URL)
    has_gemini_key = bool(settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY)
    config_healthy = has_db_url and has_gemini_key

    # Check vector store directory state (empty is healthy, directory check only)
    vector_store_healthy = True
    try:
        os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
    except Exception:
        vector_store_healthy = False

    all_ready = db_healthy and config_healthy and vector_store_healthy

    checks = {
        "database": "healthy" if db_healthy else "unhealthy",
        "vector_store": "healthy" if vector_store_healthy else "unhealthy",
        "configuration": "healthy" if config_healthy else "unhealthy"
    }

    if all_ready:
        return {
            "status": "ready",
            "checks": checks
        }
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "checks": checks
        }


@router.get("/health/llm")
async def llm_diagnostic_check(response: Response):
    """
    Manual Diagnostic LLM Endpoint.
    Performs a minimal test request to Gemini API.
    NOTE: DO NOT configure UptimeRobot to monitor this endpoint to avoid credit usage.
    """
    try:
        llm = llm_service.get_llm(temperature=0.0)
        res = await llm.ainvoke("ping")
        return {
            "status": "healthy",
            "provider": "google-gemini",
            "model": settings.GEMINI_MODEL,
            "response": str(res.content).strip()
        }
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "unhealthy",
            "provider": "google-gemini",
            "model": settings.GEMINI_MODEL,
            "error": "AI service is temporarily unavailable."
        }
