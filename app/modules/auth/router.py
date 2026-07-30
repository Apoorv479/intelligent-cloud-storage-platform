from fastapi import APIRouter, status

from app.core.responses import APIResponse, success_response
from app.modules.auth.service import auth_service
from app.modules.users.schemas import (
    UserRegisterRequest,
    UserResponse,
)
from app.modules.users.schemas import (
    TokenResponse,
    UserLoginRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[UserResponse],
)
async def register(
    request: UserRegisterRequest,
):
    """
    Register a new user.
    """

    user = await auth_service.register(request)

    return success_response(
        message="User registered successfully.",
        data=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
)
async def login(
    request: UserLoginRequest,
):
    """
    Authenticate a user.
    """

    token = await auth_service.login(request)

    return success_response(
        message="Login successful.",
        data=token,
    )
