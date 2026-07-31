from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.core.responses import APIResponse, success_response
from app.modules.folders.schemas import (
    FolderCreateRequest,
    FolderResponse,
)
from app.modules.folders.service import folder_service
from app.modules.users.models import UserDocument

router = APIRouter(
    prefix="/folders",
    tags=["Folders"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[FolderResponse],
)
async def create_folder(
    request: FolderCreateRequest,
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Create a new folder.
    """

    folder = await folder_service.create_folder(
        request,
        current_user,
    )

    return success_response(
        message="Folder created successfully.",
        data=FolderResponse.model_validate(folder),
    )
