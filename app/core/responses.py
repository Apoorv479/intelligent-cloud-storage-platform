"""
Standard API response models and helper functions.
"""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard success response.
    """

    success: bool = True
    message: str
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    success: bool = False
    message: str
    error: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedData(BaseModel, Generic[T]):
    """
    Standard paginated response payload.
    """

    items: list[T]
    total: int
    skip: int
    limit: int
    has_next: bool


def success_response(
    message: str,
    data: Any = None,
) -> APIResponse:
    """
    Generate a standardized success response.
    """

    return APIResponse(
        message=message,
        data=data,
    )


def error_response(
    message: str,
    error: Any = None,
) -> ErrorResponse:
    """
    Generate a standardized error response.
    """

    return ErrorResponse(
        message=message,
        error=error,
    )
