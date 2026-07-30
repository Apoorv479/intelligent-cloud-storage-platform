from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import NotFoundException, register_exception_handlers
from app.core.logger import logger
from app.core.responses import APIResponse

logger.info("Initializing application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Register global exception handlers
register_exception_handlers(app)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")

    return APIResponse(
        message="Application started successfully.",
        data={
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        },
    )


@app.get("/health")
async def health():
    logger.info("Health endpoint accessed.")

    return APIResponse(
        message="Health check successful.",
        data={
            "status": "healthy",
        },
    )


@app.get("/error")
async def error():
    logger.info("Error endpoint accessed.")

    raise NotFoundException("Folder does not exist.")
