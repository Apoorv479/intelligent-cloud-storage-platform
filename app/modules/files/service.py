from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.infrastructure.storage.minio_client import minio_storage
from app.modules.files.models import FileDocument
from app.modules.files.repository import file_repository
from app.modules.folders.repository import folder_repository
from app.modules.users.models import UserDocument
from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.modules.files.schemas import FileUpdateRequest


class FileService:
    """
    File business logic.
    """

    async def upload_file(
        self,
        file: UploadFile,
        folder_id: str | None,
        current_user: UserDocument,
    ) -> FileDocument:
        """
        Upload a file to object storage and save its metadata.
        """

        # Validate target folder

        if folder_id is not None:
            folder = await folder_repository.get_by_id(
                folder_id,
            )

            if folder is None:
                raise NotFoundException("Folder not found.")

            if folder.user_id != current_user.id:
                raise NotFoundException("Folder not found.")

            if folder.is_deleted:
                raise NotFoundException("Folder not found.")

        # Validate filename

        if not file.filename:
            raise ValueError("File name is required.")

        original_name = file.filename

        # Read uploaded file

        data = await file.read()

        if not data:
            raise ValueError("File cannot be empty.")

        # Generate unique storage name

        extension = Path(original_name).suffix

        storage_name = f"{uuid4().hex}{extension}"

        # Keep every user's objects isolated.

        storage_path = f"{current_user.id}/{storage_name}"

        content_type = file.content_type or "application/octet-stream"

        # Upload to MinIO

        minio_storage.upload_file(
            object_name=storage_path,
            data=data,
            content_type=content_type,
        )

        # Create MongoDB metadata

        file_document = FileDocument(
            user_id=current_user.id,
            folder_id=folder_id,
            original_name=original_name,
            storage_name=storage_name,
            content_type=content_type,
            size=len(data),
            storage_path=storage_path,
        )

        try:
            return await file_repository.create(
                file_document,
            )

        except Exception:
            # MinIO succeeded but MongoDB failed.
            # Remove the orphaned MinIO object.

            minio_storage.delete_file(
                storage_path,
            )

            raise

    async def get_files(
        self,
        current_user: UserDocument,
        folder_id: str | None = None,
    ) -> list[FileDocument]:
        """
        Retrieve files belonging to the current user.

        If folder_id is provided, retrieve files
        belonging to that folder.
        """

        filters = {
            "user_id": current_user.id,
            "is_deleted": False,
        }

        if folder_id is not None:
            folder = await folder_repository.get_by_id(
                folder_id,
            )

            if folder is None:
                raise NotFoundException("Folder not found.")

            if folder.user_id != current_user.id:
                raise NotFoundException("Folder not found.")

            if folder.is_deleted:
                raise NotFoundException("Folder not found.")

            filters["folder_id"] = folder_id

        return await file_repository.get_many(
            filters=filters,
        )

    async def get_file_by_id(
        self,
        file_id: str,
        current_user: UserDocument,
    ) -> FileDocument:
        """
        Retrieve a file by id.
        """

        file_document = await file_repository.get_by_id(
            file_id,
        )

        if file_document is None:
            raise NotFoundException("File not found.")

        if file_document.user_id != current_user.id:
            raise NotFoundException("File not found.")

        if file_document.is_deleted:
            raise NotFoundException("File not found.")

        return file_document

    async def download_file(
        self,
        file_id: str,
        current_user: UserDocument,
    ) -> tuple[FileDocument, bytes]:
        """
        Retrieve file metadata and download its content.
        """

        file_document = await self.get_file_by_id(
            file_id=file_id,
            current_user=current_user,
        )

        data = minio_storage.download_file(
            file_document.storage_path,
        )

        return file_document, data

    async def delete_file(
        self,
        file_id: str,
        current_user: UserDocument,
    ) -> FileDocument:
        """
        Soft delete a file.
        """

        file_document = await self.get_file_by_id(
            file_id=file_id,
            current_user=current_user,
        )

        deleted_file = await file_repository.update(
            file_document.id,
            {
                "is_deleted": True,
            },
        )

        if deleted_file is None:
            raise NotFoundException("File not found.")

        return deleted_file

    async def rename_file(
        self,
        file_id: str,
        request: FileUpdateRequest,
        current_user: UserDocument,
    ) -> FileDocument:
        """
        Rename a file.

        Only the user-visible filename is changed.
        The internal MinIO object name remains unchanged.
        """

        file_document = await self.get_file_by_id(
            file_id=file_id,
            current_user=current_user,
        )

        existing_file = await file_repository.get_one(
            {
                "user_id": current_user.id,
                "folder_id": file_document.folder_id,
                "original_name": request.name,
                "is_deleted": False,
            }
        )

        if existing_file is not None and existing_file.id != file_document.id:
            raise ConflictException("A file with this name already exists.")

        updated_file = await file_repository.update(
            file_document.id,
            {
                "original_name": request.name,
            },
        )

        if updated_file is None:
            raise NotFoundException("File not found.")

        return updated_file

    async def get_trash(
        self,
        current_user: UserDocument,
    ) -> list[FileDocument]:
        """
        Retrieve soft-deleted files belonging to the current user.
        """

        return await file_repository.get_many(
            filters={
                "user_id": current_user.id,
                "is_deleted": True,
            },
        )

    async def restore_file(
        self,
        file_id: str,
        current_user: UserDocument,
    ) -> FileDocument:
        """
        Restore a soft-deleted file.
        """

        file_document = await file_repository.get_by_id(
            file_id,
        )

        if file_document is None:
            raise NotFoundException("File not found.")

        if file_document.user_id != current_user.id:
            raise NotFoundException("File not found.")

        if not file_document.is_deleted:
            raise ConflictException("File is not deleted.")

        # Check whether an active file with the same
        # name already exists in the same folder.

        existing_file = await file_repository.get_one(
            {
                "user_id": current_user.id,
                "folder_id": file_document.folder_id,
                "original_name": file_document.original_name,
                "is_deleted": False,
            }
        )

        if existing_file is not None:
            raise ConflictException("A file with this name already exists.")

        restored_file = await file_repository.update(
            file_document.id,
            {
                "is_deleted": False,
            },
        )

        if restored_file is None:
            raise NotFoundException("File not found.")

        return restored_file

    async def permanently_delete_file(
        self,
        file_id: str,
        current_user: UserDocument,
    ) -> None:
        """
        Permanently delete a file from MinIO and MongoDB.

        The file must already be in trash.
        """

        file_document = await file_repository.get_by_id(
            file_id,
        )

        if file_document is None:
            raise NotFoundException("File not found.")

        if file_document.user_id != current_user.id:
            raise NotFoundException("File not found.")

        if not file_document.is_deleted:
            raise ConflictException(
                "File must be moved to trash before permanent deletion."
            )

        # Delete actual object from MinIO.

        minio_storage.delete_file(
            file_document.storage_path,
        )

        # Delete metadata permanently from MongoDB.

        deleted = await file_repository.delete(
            file_document.id,
        )

        if not deleted:
            raise NotFoundException("File not found.")


file_service = FileService()
