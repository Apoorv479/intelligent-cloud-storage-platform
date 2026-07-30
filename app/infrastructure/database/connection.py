"""
MongoDB connection management.
"""

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from app.core.config import settings
from app.core.logger import logger


class MongoDB:

    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.database: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:

        logger.info("Connecting to MongoDB...")

        self.client = AsyncIOMotorClient(settings.MONGODB_URI)

        self.database = self.client[settings.MONGODB_DATABASE]

        logger.info("MongoDB connection established.")

    async def disconnect(self) -> None:

        logger.info("Closing MongoDB connection...")

        if self.client:
            self.client.close()

        logger.info("MongoDB connection closed.")


mongodb = MongoDB()
