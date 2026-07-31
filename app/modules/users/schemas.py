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


class UserRegisterRequest(BaseModel):
    """
    Request schema for user registration.
    """

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLoginRequest(BaseModel):
    """
    Request schema for user login.
    """

    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    """
    Authentication token response.
    """

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Request schema for refreshing an access token.
    """

    refresh_token: str


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
