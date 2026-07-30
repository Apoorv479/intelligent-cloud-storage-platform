from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateRequest(BaseModel):
    """
    Request schema for creating a user.
    """

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )


class UserResponse(BaseModel):
    """
    Response schema for a user.
    """

    id: str

    email: EmailStr

    full_name: str

    is_active: bool

    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
