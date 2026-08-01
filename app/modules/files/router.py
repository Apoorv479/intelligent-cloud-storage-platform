from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)

from app.core.dependencies import get_current_user
from app.core.responses import (
    APIResponse,
    success_response,
)
from app.modules.files.schemas import FileResponse
from app.modules.files.service import file_service
from app.modules.users.models import UserDocument

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[FileResponse],
)
async def upload_file(
    file: UploadFile = File(...),
    folder_id: str | None = Form(default=None),
    current_user: UserDocument = Depends(
        get_current_user,
    ),
):
    """
    Upload a file.
    """

    uploaded_file = await file_service.upload_file(
        file=file,
        folder_id=folder_id,
        current_user=current_user,
    )

    return success_response(
        message="File uploaded successfully.",
        data=FileResponse.model_validate(
            uploaded_file,
        ),
    )


@router.get(
    "",
    response_model=APIResponse[list[FileResponse]],
)
async def get_files(
    folder_id: str | None = None,
    current_user: UserDocument = Depends(
        get_current_user,
    ),
):
    """
    Retrieve files belonging to the authenticated user.
    """

    files = await file_service.get_files(
        current_user=current_user,
        folder_id=folder_id,
    )

    return success_response(
        message="Files retrieved successfully.",
        data=[FileResponse.model_validate(file) for file in files],
    )


@router.get(
    "/{file_id}",
    response_model=APIResponse[FileResponse],
)
async def get_file(
    file_id: str,
    current_user: UserDocument = Depends(
        get_current_user,
    ),
):
    """
    Retrieve a file by id.
    """

    file_document = await file_service.get_file_by_id(
        file_id=file_id,
        current_user=current_user,
    )

    return success_response(
        message="File retrieved successfully.",
        data=FileResponse.model_validate(
            file_document,
        ),
    )
