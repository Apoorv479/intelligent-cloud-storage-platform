from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.exceptions import NotFoundException
from app.infrastructure.storage.minio_client import minio_storage
from app.modules.files.models import FileDocument
from app.modules.files.repository import file_repository
from app.modules.folders.repository import folder_repository
from app.modules.users.models import UserDocument


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


file_service = FileService()
