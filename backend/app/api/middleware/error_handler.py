"""
Global error handlers for FastAPI.
Converts unhandled exceptions into standardized JSON error responses.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
import traceback

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "status_code": 500},
    )
