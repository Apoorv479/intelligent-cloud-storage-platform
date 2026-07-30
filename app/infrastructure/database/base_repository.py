from abc import ABC
from typing import Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection

from app.infrastructure.database.base_model import BaseDocument
from app.infrastructure.database.connection import mongodb

T = TypeVar("T", bound=BaseDocument)


class BaseRepository(Generic[T], ABC):
    """
    Generic MongoDB repository.
    """

    collection_name: str

    document_class: type[T]

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if mongodb.database is None:
            raise RuntimeError("MongoDB is not connected.")

        return mongodb.database[self.collection_name]

    async def create(self, document: T) -> T:
        """
        Insert a document into MongoDB.
        """

        await self.collection.insert_one(document.model_dump(by_alias=True))

        return document
