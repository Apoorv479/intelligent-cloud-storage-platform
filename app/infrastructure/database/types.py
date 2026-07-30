"""
Common MongoDB types.
"""

from typing import Annotated

from bson import ObjectId
from pydantic import BeforeValidator


def validate_object_id(value: str | ObjectId) -> str:
    """
    Convert ObjectId to string and validate it.
    """

    if isinstance(value, ObjectId):
        return str(value)

    if ObjectId.is_valid(value):
        return value

    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    str,
    BeforeValidator(validate_object_id),
]
