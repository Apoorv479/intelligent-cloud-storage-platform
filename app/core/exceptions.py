"""
Custom application exceptions and global exception handlers.
"""

from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.core.responses import error_response

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
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error = error

        super().__init__(message)


# Authentication Exceptions


class AuthenticationException(AppException):
    """
    Raised when user authentication fails.
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationException(AppException):
    """
    Raised when a user is not authorized to access a resource.
    """

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


# Validation Exceptions


class ValidationException(AppException):
    """
    Raised when request validation fails.
    """

    def __init__(
        self,
        message: str = "Validation failed",
        error: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error=error,
        )


# Resource Exceptions


class NotFoundException(AppException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ConflictException(AppException):
    """
    Raised when a resource already exists.
    """

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


# Storage Exceptions


class StorageException(AppException):
    """
    Raised for storage-related failures.
    """

    def __init__(self, message: str = "Storage operation failed") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# AI Exceptions


class AIProcessingException(AppException):
    """
    Raised when AI processing fails.
    """

    def __init__(self, message: str = "AI processing failed") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Search Exceptions


class SearchException(AppException):
    """
    Raised when search fails.
    """

    def __init__(self, message: str = "Search failed") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Global Exception Handlers


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Handles all custom application exceptions.
    """

    logger.error(f"{request.method} {request.url.path} -> {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
            error=exc.error,
        ).model_dump(mode="json"),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handles unexpected exceptions.
    """

    logger.exception(f"{request.method} {request.url.path} -> {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="Internal server error",
            error=str(exc),
        ).model_dump(mode="json"),
    )


# Register Exception Handlers


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )
