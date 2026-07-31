from abc import ABC
from typing import Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection

from app.infrastructure.database.base_model import BaseDocument
from app.infrastructure.database.connection import mongodb
from app.infrastructure.database.types import is_valid_object_id

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

    async def create(
        self,
        document: T,
    ) -> T:
        """
        Insert a document into MongoDB.
        """

        await self.collection.insert_one(document.model_dump(by_alias=True))

        return document

    async def get_by_id(
        self,
        document_id: str,
    ) -> T | None:
        """
        Retrieve a document by its MongoDB id.
        """

        if not is_valid_object_id(document_id):
            return None

        document = await self.collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return self.document_class.model_validate(document)

    async def get_one(
        self,
        filters: dict,
    ) -> T | None:
        """
        Retrieve a single document matching the given filters.
        """

        document = await self.collection.find_one(filters)

        if document is None:
            return None

        return self.document_class.model_validate(document)

    async def get_many(
        self,
        filters: dict | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """
        Retrieve multiple documents matching the given filters.
        """

        filters = filters or {}

        cursor = self.collection.find(filters).skip(skip).limit(limit)

        documents = await cursor.to_list(length=limit)

        return [self.document_class.model_validate(document) for document in documents]

    async def count(
        self,
        filters: dict | None = None,
    ) -> int:
        """
        Count documents matching the given filters.
        """

        filters = filters or {}

        return await self.collection.count_documents(filters)

    async def update(
        self,
        document_id: str,
        update_data: dict,
    ) -> T | None:
        """
        Update a document.
        """

        if not is_valid_object_id(document_id):
            return None

        await self.collection.update_one(
            {
                "_id": document_id,
            },
            {
                "$set": update_data,
            },
        )

        document = await self.collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return self.document_class.model_validate(document)
