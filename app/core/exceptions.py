"""
Custom application exceptions and global exception handlers.
"""

from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logger import logger

# Base Exception


class AppException(Exception):
    """
    Base exception for the entire application.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        error: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error = error

        super().__init__(message)


# Authentication


class AuthenticationException(AppException):

    def __init__(self, message="Authentication failed"):
        super().__init__(
            message,
            status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationException(AppException):

    def __init__(self, message="Access denied"):
        super().__init__(
            message,
            status.HTTP_403_FORBIDDEN,
        )


# Validation


class ValidationException(AppException):

    def __init__(
        self,
        message="Validation failed",
        error=None,
    ):
        super().__init__(
            message,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            error,
        )


# Resources


class NotFoundException(AppException):

    def __init__(self, message="Resource not found"):
        super().__init__(
            message,
            status.HTTP_404_NOT_FOUND,
        )


class ConflictException(AppException):

    def __init__(self, message="Resource already exists"):
        super().__init__(
            message,
            status.HTTP_409_CONFLICT,
        )


# Storage


class StorageException(AppException):

    def __init__(self, message="Storage operation failed"):
        super().__init__(
            message,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# AI


class AIProcessingException(AppException):

    def __init__(self, message="AI processing failed"):
        super().__init__(
            message,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Search


class SearchException(AppException):

    def __init__(self, message="Search failed"):
        super().__init__(
            message,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Global Exception Handler


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """
    Handles all custom application exceptions.
    """

    logger.error(f"{request.method} {request.url.path} -> {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error": exc.error,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handles unexpected exceptions.
    """

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# Register handlers


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )
