"""
Standard API response models.

Every API endpoint should return one of these response models.
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

    message: str = "Request completed successfully."

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
