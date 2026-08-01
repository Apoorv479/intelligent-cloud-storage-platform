from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.core.responses import APIResponse, success_response
from app.modules.folders.schemas import (
    FolderCreateRequest,
    FolderUpdateRequest,
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


@router.get(
    "",
    response_model=APIResponse[list[FolderResponse]],
)
async def get_folders(
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Retrieve all folders for the authenticated user.
    """

    folders = await folder_service.get_folders(current_user)

    return success_response(
        message="Folders retrieved successfully.",
        data=[FolderResponse.model_validate(folder) for folder in folders],
    )


@router.get(
    "/{folder_id}",
    response_model=APIResponse[FolderResponse],
)
async def get_folder(
    folder_id: str,
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Retrieve a folder by id.
    """

    folder = await folder_service.get_folder_by_id(
        folder_id,
        current_user,
    )

    return success_response(
        message="Folder retrieved successfully.",
        data=FolderResponse.model_validate(folder),
    )


@router.patch(
    "/{folder_id}",
    response_model=APIResponse[FolderResponse],
)
async def rename_folder(
    folder_id: str,
    request: FolderUpdateRequest,
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Rename a folder.
    """

    folder = await folder_service.rename_folder(
        folder_id,
        request,
        current_user,
    )

    return success_response(
        message="Folder renamed successfully.",
        data=FolderResponse.model_validate(folder),
    )


@router.delete(
    "/{folder_id}",
    response_model=APIResponse[FolderResponse],
)
async def delete_folder(
    folder_id: str,
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Soft delete a folder.
    """

    folder = await folder_service.delete_folder(
        folder_id,
        current_user,
    )

    return success_response(
        message="Folder deleted successfully.",
        data=FolderResponse.model_validate(folder),
    )
