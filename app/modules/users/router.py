from fastapi import APIRouter, status

from app.core.responses import success_response
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
)
async def create_user(
    request: UserCreateRequest,
):
    user = await user_service.create_user(request)

    return success_response(
        message="User created successfully.",
        data=UserResponse.model_validate(user),
    )
