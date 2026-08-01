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
