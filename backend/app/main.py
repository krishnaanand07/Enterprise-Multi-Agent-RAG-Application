"""
Enterprise Multi-Agent RAG Research Assistant — FastAPI Application

This is the main entry point for the backend API.
It configures the FastAPI application, middleware, and routes.
"""

import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.settings import settings
from app.database.session import engine
from app.database.base import Base
import app.models  # Import all models to register them with Base


# ── Application Lifespan ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.

    Startup:
      - Log startup environment & configuration metadata
      - Verify and initialize database schema (with safety try/except)

    Shutdown:
      - Close database connection pool
    """
    logger.info(f"=== Starting {settings.APP_NAME} v{settings.APP_VERSION} ===")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"LLM Provider Configured: {settings.LLM_PROVIDER}")

    # Database connection & schema migration check
    try:
        logger.info("Initializing database connection pool and creating tables if missing...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            from sqlalchemy import text
            await conn.execute(text("ALTER TABLE messages ADD COLUMN IF NOT EXISTS chart_data JSONB;"))
        logger.info("Database connection and schema initialization successful.")
    except Exception as e:
        logger.error(f"Database initialization error during startup: {e}")
        logger.warning("Application starting in degraded mode — database may be cold-starting or unavailable.")

    yield  # Application is running

    # Shutdown tasks
    logger.info("Shutting down application and disposing connection pool...")
    try:
        await engine.dispose()
        logger.info("Database engine disposed successfully.")
    except Exception as e:
        logger.error(f"Error disposing database engine: {e}")


from app.api.routes import api_router
from app.api.middleware.error_handler import global_exception_handler

# ── Create FastAPI Application ────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A production-ready AI platform for interacting with private "
        "knowledge bases using natural language. Features multi-agent "
        "architecture with RAG, SQL, web search, and code execution."
    ),
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Register exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Register API router
app.include_router(api_router, prefix="/api")


# ── CORS Middleware ───────────────────────────────────────────
raw_origins = settings.ALLOWED_ORIGINS.strip()
origins = []
if raw_origins.startswith("[") and raw_origins.endswith("]"):
    try:
        parsed = json.loads(raw_origins)
        if isinstance(parsed, list):
            origins = [str(o).strip().rstrip('/') for o in parsed if str(o).strip()]
    except Exception:
        pass
if not origins:
    origins = [origin.strip().rstrip('/') for origin in raw_origins.split(",") if origin.strip()]

allow_credentials = True
if "*" in origins:
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Lightweight Health Check Endpoints ─────────────────────────
@app.get("/health", tags=["Health"])
async def root_health_check():
    """
    Extremely lightweight health check endpoint required for Render cold-starts
    and uptime pinging. Returns 200 OK without initializing heavy AI/ML libraries.
    """
    return {"status": "healthy"}


@app.get("/api/health", tags=["Health"])
async def api_health_check():
    """
    API Health check endpoint.
    Returns status and version information without initializing heavy AI/ML libraries.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# ── Root ──────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
