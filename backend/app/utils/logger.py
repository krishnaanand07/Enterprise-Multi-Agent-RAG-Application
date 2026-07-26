"""
Logging configuration using Loguru.

Provides structured, colorized logging with file rotation.

Usage:
    from loguru import logger

    logger.info("Server started")
    logger.error("Something went wrong", exc_info=True)
"""

import sys
from loguru import logger

from app.config.settings import settings


def setup_logging():
    """
    Configure application logging.

    - Console output with colors
    - File output with rotation (10MB max, 7 days retention)
    - Structured format for production
    """
    # Remove default handler
    logger.remove()

    # Console handler — colorized output
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File handler — rotated logs
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    logger.info(f"Logging configured — level: {settings.LOG_LEVEL}")
