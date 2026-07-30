from datetime import datetime

from pydantic import EmailStr, Field

from app.infrastructure.database.base_model import BaseDocument


class UserDocument(BaseDocument):
    """
    MongoDB document representing a user.
    """

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    hashed_password: str

    is_active: bool = True

    is_verified: bool = False

    last_login: datetime | None = None

    refresh_token_version: int = 0
