from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger

logger.info("Initializing application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.on_event("startup")
async def startup():
    logger.info("Application started successfully.")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Application stopped.")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health():
    logger.info("Health endpoint accessed.")

    return {"status": "healthy"}
