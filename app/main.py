from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import (
    NotFoundException,
    register_exception_handlers,
)
from app.core.lifespan import lifespan
from app.core.logger import logger
from app.core.responses import success_response
from app.modules.users.router import router as user_router

# from app.repositories.test_repository import TestRepository

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(user_router)
# test_repository = TestRepository()

register_exception_handlers(app)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")

    return success_response(
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

    return success_response(
        message="Health check successful.",
        data={
            "status": "healthy",
        },
    )


@app.get("/error")
async def error():
    logger.info("Error endpoint accessed.")

    raise NotFoundException("Folder does not exist.")


# @app.get("/db")
# async def database_check():
#     await test_repository.ping()

#     return success_response(
#         message="MongoDB connection is working.",
#         data={
#             "database": settings.MONGODB_DATABASE,
#         },
#     )
