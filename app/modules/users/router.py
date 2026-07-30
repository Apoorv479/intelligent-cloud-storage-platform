from fastapi import APIRouter, status

from app.core.responses import APIResponse, success_response
from app.modules.users.schemas import (
    UserCreateRequest,
    UserResponse,
)
from app.modules.users.service import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[UserResponse],
)
async def create_user(
    request: UserCreateRequest,
):
    """
    Create a new user.
    """

    user = await user_service.create_user(request)

    return success_response(
        message="User created successfully.",
        data=UserResponse.model_validate(user),
    )


@router.get(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
)
async def get_user(
    user_id: str,
):
    """
    Retrieve a user by id.
    """

    user = await user_service.get_user_by_id(user_id)

    return success_response(
        message="User retrieved successfully.",
        data=UserResponse.model_validate(user),
    )
