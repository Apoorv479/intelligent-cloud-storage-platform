from fastapi import APIRouter, status

from app.core.responses import APIResponse, success_response
from app.modules.auth.service import auth_service
from app.modules.users.schemas import (
    UserRegisterRequest,
    UserResponse,
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
