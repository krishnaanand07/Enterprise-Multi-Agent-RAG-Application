import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.database import engine, Base
from app.api.routes import auth, documents, chat, users, health

logger = logging.getLogger("enterprise_rag")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation and safe logging
    logger.info("Application starting - Enterprise RAG Assistant v2.0.0")

    if settings.DATABASE_URL:
        logger.info("Database configuration detected")
    else:
        logger.error("DATABASE_URL configuration is missing")

    if not (settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY):
        logger.error("GEMINI_API_KEY is missing")

    # Initialize DB tables on startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database table initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization warning: {str(e)}")

    # Ensure storage directories exist (cold start safe)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Health & Monitoring Routers (Root /api level)
app.include_router(health.router, prefix="/api")

# Include API Routers (/api/v1 level)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

# Mount Static Frontend Files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
