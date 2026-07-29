from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.core.responses import APIResponse

logger.info("Initializing application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/", response_model=APIResponse)
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


@app.get("/health", response_model=APIResponse)
async def health():
    logger.info("Health endpoint accessed.")

    return APIResponse(
        message="Health check successful.",
        data={"status": "healthy"},
    )
