"""
Application-wide constants.

This module contains all reusable constants and enums used throughout
the Intelligent Cloud Storage Platform.
"""

from enum import Enum

# API


API_V1_PREFIX = "/api/v1"

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# File Upload


MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB

DEFAULT_CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB


# Environment


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


# User Roles


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


# Account Status


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# File Status


class FileStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DELETED = "deleted"


# Folder Status


class FolderStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


# Storage Providers


class StorageProvider(str, Enum):
    MINIO = "minio"
    AWS_S3 = "aws_s3"


# AI Processing


class AIStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# Search


class SearchType(str, Enum):
    KEYWORD = "keyword"
    SEMANTIC = "semantic"


# Notification


class NotificationType(str, Enum):
    EMAIL = "email"
    SYSTEM = "system"


# HTTP Messages


SUCCESS = "Success"

FAILED = "Failed"

NOT_FOUND = "Resource not found"

UNAUTHORIZED = "Unauthorized"

FORBIDDEN = "Forbidden"

VALIDATION_ERROR = "Validation Error"
