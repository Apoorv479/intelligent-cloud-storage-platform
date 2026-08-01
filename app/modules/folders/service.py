from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.modules.folders.models import FolderDocument
from app.modules.folders.repository import folder_repository
from app.modules.folders.schemas import (
    FolderCreateRequest,
    FolderUpdateRequest,
)
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

    async def get_folders(
        self,
        current_user: UserDocument,
    ) -> list[FolderDocument]:
        """
        Retrieve all folders of the current user.
        """

        return await folder_repository.get_many(
            filters={
                "user_id": current_user.id,
                "is_deleted": False,
            }
        )

    async def get_folder_by_id(
        self,
        folder_id: str,
        current_user: UserDocument,
    ) -> FolderDocument:
        """
        Retrieve a folder by id.
        """

        folder = await folder_repository.get_by_id(folder_id)

        if folder is None:
            raise NotFoundException("Folder not found.")

        if folder.user_id != current_user.id:
            raise NotFoundException("Folder not found.")

        if folder.is_deleted:
            raise NotFoundException("Folder not found.")

        return folder

    async def rename_folder(
        self,
        folder_id: str,
        request: FolderUpdateRequest,
        current_user: UserDocument,
    ) -> FolderDocument:
        """
        Rename a folder and update paths of all descendants.
        """

        folder = await folder_repository.get_by_id(folder_id)

        if folder is None:
            raise NotFoundException("Folder not found.")

        if folder.user_id != current_user.id:
            raise NotFoundException("Folder not found.")

        if folder.is_deleted:
            raise NotFoundException("Folder not found.")

        # Check for another folder with the same name
        # under the same parent.
        existing_folder = await folder_repository.get_one(
            {
                "user_id": current_user.id,
                "parent_folder_id": folder.parent_folder_id,
                "name": request.name,
                "is_deleted": False,
            }
        )

        if existing_folder is not None and existing_folder.id != folder.id:
            raise ConflictException("Folder already exists.")

        old_path = folder.path

        # Build the new folder path.
        if folder.parent_folder_id is None:
            new_path = f"/{request.name}"

        else:
            parent = await folder_repository.get_by_id(
                folder.parent_folder_id,
            )

            if parent is None:
                raise NotFoundException("Parent folder not found.")

            new_path = f"{parent.path}/{request.name}"

        # Update the folder itself.
        updated_folder = await folder_repository.update(
            folder.id,
            {
                "name": request.name,
                "path": new_path,
            },
        )

        # Find all descendants.
        descendants = await folder_repository.get_many(
            filters={
                "user_id": current_user.id,
                "path": {"$regex": f"^{old_path}/"},
            },
            limit=1000,
        )

        # Update every descendant path.
        for descendant in descendants:

            descendant_new_path = descendant.path.replace(
                old_path,
                new_path,
                1,
            )

            await folder_repository.update(
                descendant.id,
                {
                    "path": descendant_new_path,
                },
            )

        return updated_folder

    async def delete_folder(
        self,
        folder_id: str,
        current_user: UserDocument,
    ) -> FolderDocument:
        """
        Soft delete a folder and all of its descendants.
        """

        folder = await folder_repository.get_by_id(folder_id)

        if folder is None:
            raise NotFoundException("Folder not found.")

        if folder.user_id != current_user.id:
            raise NotFoundException("Folder not found.")

        if folder.is_deleted:
            raise NotFoundException("Folder not found.")

        # Soft delete the requested folder.
        deleted_folder = await folder_repository.update(
            folder.id,
            {
                "is_deleted": True,
            },
        )

        # Find all descendant folders.
        descendants = await folder_repository.get_many(
            filters={
                "user_id": current_user.id,
                "path": {"$regex": f"^{folder.path}/"},
                "is_deleted": False,
            },
            limit=1000,
        )

        # Soft delete every descendant.
        for descendant in descendants:

            await folder_repository.update(
                descendant.id,
                {
                    "is_deleted": True,
                },
            )

        return deleted_folder


folder_service = FolderService()
