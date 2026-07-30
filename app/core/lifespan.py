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
from app.infrastructure.database.connection import mongodb
from app.core.config import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    """

    # ======================================================
    # Startup
    # ======================================================

    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Version      : {settings.APP_VERSION}")
    logger.info(f"Environment  : {settings.ENVIRONMENT}")
    logger.info("=" * 60)

    try:
        # --------------------------------------------------
        # Future Initializations
        # --------------------------------------------------
        #
        await mongodb.connect()
        # await initialize_redis()
        # await initialize_minio()
        # await initialize_qdrant()
        # await load_ai_models()
        # await start_background_workers()
        #
        # --------------------------------------------------

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
        # Future Cleanup
        # --------------------------------------------------
        #
        await mongodb.disconnect()
        # await close_redis()
        # await close_minio()
        # await close_qdrant()
        # await stop_background_workers()
        #
        # --------------------------------------------------

        logger.info("Application shutdown completed successfully.")
