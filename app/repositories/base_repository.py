"""
Base repository for MongoDB collections.
"""

from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.infrastructure.database.connection import mongodb


class BaseRepository:
    """
    Base repository providing common MongoDB collection access.

    Child repositories should inherit from this class.
    """

    collection_name: str

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return the MongoDB collection.
        """
        if mongodb.database is None:
            raise RuntimeError("MongoDB is not connected.")

        return mongodb.database[self.collection_name]

    async def ping(self) -> bool:
        """
        Simple check to verify repository access.
        """
        await self.collection.estimated_document_count()
        return True
