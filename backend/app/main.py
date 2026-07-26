"""
Enterprise Multi-Agent RAG Research Assistant — FastAPI Application

This is the main entry point for the backend API.
It configures the FastAPI application, middleware, and routes.
"""

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
      - Initialize database connection pool
      - Load embedding model
      - Initialize vector store

    Shutdown:
      - Close database connections
      - Clean up resources
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")

    # Startup tasks will be added in later phases
    # - Database initialization (Phase 2)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        from sqlalchemy import text
        await conn.execute(text("ALTER TABLE messages ADD COLUMN IF NOT EXISTS chart_data JSONB;"))

    # - Embedding model loading (Phase 4)
    # - Vector store initialization (Phase 4)

    yield  # Application is running

    # Shutdown tasks
    logger.info("Shutting down application...")


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
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns application status and version information.
    Used by Docker health checks and monitoring systems.
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
