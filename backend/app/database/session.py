"""
Database session configuration.

Uses SQLAlchemy 2.0 async engine with asyncpg driver.
Provides an async session factory for dependency injection.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from app.config.settings import settings


def _format_asyncpg_url(url: str) -> str:
    """Format connection string for SQLAlchemy asyncpg compatibility."""
    if not url or "sqlite" in url:
        return url

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        has_sslmode = "sslmode" in query_params

        # Remove libpq parameters unsupported by asyncpg
        unsupported_params = ["channel_binding", "sslmode", "target_session_attrs", "gssencmode"]
        for param in unsupported_params:
            query_params.pop(param, None)

        # Set ssl=require for cloud hosts (Neon, Render, Supabase)
        if "ssl" not in query_params and (has_sslmode or (parsed.hostname and parsed.hostname not in ("localhost", "127.0.0.1"))):
            query_params["ssl"] = ["require"]

        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
    except Exception:
        return url


db_url = _format_asyncpg_url(settings.DATABASE_URL)

# ── Async Engine ──────────────────────────────────────────────
# Configured for cloud DB resilience (Render PostgreSQL)
engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=5,
    pool_timeout=15,
    pool_recycle=300,
    pool_pre_ping=True,
)

# ── Session Factory ───────────────────────────────────────────
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ── Dependency ────────────────────────────────────────────────
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.

    Usage in routes:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
