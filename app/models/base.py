from datetime import UTC, datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class BaseDocument(BaseModel):
    """
    Base model inherited by every MongoDB document.
    """

    id: str = Field(
        default_factory=lambda: str(ObjectId()),
        alias="_id",
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
