"""
Application lifespan management.

This module is responsible for handling application startup
and shutdown events.

Future responsibilities:
- Initialize MongoDB
- Initialize Redis
- Initialize MinIO
- Initialize Qdrant
- Load AI models
- Start background workers
- Gracefully close all connections
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.infrastructure.database.connection import mongodb
from app.infrastructure.storage.minio_client import minio_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    """

    # ==================================================
    # Startup
    # ==================================================

    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Version      : {settings.APP_VERSION}")
    logger.info(f"Environment  : {settings.ENVIRONMENT}")
    logger.info("=" * 60)

    try:
        # --------------------------------------------------
        # Initialize MongoDB
        # --------------------------------------------------

        await mongodb.connect()

        # --------------------------------------------------
        # Initialize MinIO
        # --------------------------------------------------

        logger.info("Initializing MinIO storage...")

        minio_storage.ensure_bucket()

        logger.info("MinIO storage initialized.")

        # --------------------------------------------------
        # Future Initializations
        # --------------------------------------------------

        # await initialize_redis()
        # await initialize_qdrant()
        # await load_ai_models()
        # await start_background_workers()

        logger.info("Application startup completed successfully.")

        yield

    except Exception as exc:
        logger.exception(f"Application startup failed: {exc}")
        raise

    finally:

        # ==================================================
        # Shutdown
        # ==================================================

        logger.info("Shutting down application...")

        # --------------------------------------------------
        # MongoDB Cleanup
        # --------------------------------------------------

        await mongodb.disconnect()

        # --------------------------------------------------
        # Future Cleanup
        # --------------------------------------------------

        # await close_redis()
        # await close_qdrant()
        # await stop_background_workers()

        logger.info("Application shutdown completed successfully.")
