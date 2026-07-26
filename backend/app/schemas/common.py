"""
Common Pydantic schemas used across the application.
"""

from typing import Optional, Any
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Generic success response."""
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Generic error response."""
    detail: str
    status_code: int


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
