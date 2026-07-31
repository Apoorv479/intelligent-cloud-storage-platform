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

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends

from app.core.dependencies import get_current_user
from app.modules.users.models import UserDocument

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


@router.post(
    "/token",
    response_model=TokenResponse,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 endpoint used by Swagger Authorize.
    """

    request = UserLoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    return await auth_service.login(request)


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
)
async def get_me(
    current_user: UserDocument = Depends(
        get_current_user,
    ),
):
    """
    Return the authenticated user.
    """

    return success_response(
        message="Current user fetched successfully.",
        data=UserResponse.model_validate(
            current_user,
        ),
    )
