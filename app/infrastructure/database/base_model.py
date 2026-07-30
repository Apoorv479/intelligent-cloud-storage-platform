from datetime import UTC, datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.infrastructure.database.types import PyObjectId


class BaseDocument(BaseModel):
    """
    Base document inherited by every MongoDB model.
    """

    id: PyObjectId = Field(
        default_factory=lambda: str(ObjectId()),
        alias="_id",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            ObjectId: str,
        },
    )
