from typing import Annotated

from bson import ObjectId
from pydantic import BeforeValidator


def validate_object_id(value: str | ObjectId) -> str:
    if isinstance(value, ObjectId):
        return str(value)

    if ObjectId.is_valid(value):
        return value

    raise ValueError("Invalid ObjectId")


def is_valid_object_id(value: str) -> bool:
    return ObjectId.is_valid(value)


PyObjectId = Annotated[
    str,
    BeforeValidator(validate_object_id),
]
