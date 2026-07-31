from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.modules.folders.models import FolderDocument
from app.modules.folders.repository import folder_repository
from app.modules.folders.schemas import FolderCreateRequest
from app.modules.users.models import UserDocument


class FolderService:
    """
    Folder business logic.
    """

    async def create_folder(
        self,
        request: FolderCreateRequest,
        current_user: UserDocument,
    ) -> FolderDocument:
        """
        Create a new folder.
        """

        parent_path = ""

        if request.parent_folder_id is not None:

            parent = await folder_repository.get_by_id(
                request.parent_folder_id,
            )

            if parent is None:
                raise NotFoundException("Parent folder not found.")

            if parent.user_id != current_user.id:
                raise NotFoundException("Parent folder not found.")

            parent_path = parent.path

        existing_folder = await folder_repository.get_one(
            {
                "user_id": current_user.id,
                "parent_folder_id": request.parent_folder_id,
                "name": request.name,
                "is_deleted": False,
            }
        )

        if existing_folder is not None:
            raise ConflictException("Folder already exists.")

        path = f"{parent_path}/{request.name}" if parent_path else f"/{request.name}"

        folder = FolderDocument(
            user_id=current_user.id,
            parent_folder_id=request.parent_folder_id,
            name=request.name,
            path=path,
        )

        return await folder_repository.create(folder)


folder_service = FolderService()
