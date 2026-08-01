from pydantic import Field

from app.infrastructure.database.base_model import BaseDocument


class FileDocument(BaseDocument):
    """
    MongoDB document representing a stored file.
    """

    user_id: str

    folder_id: str | None = None

    original_name: str = Field(
        min_length=1,
        max_length=255,
    )

    storage_name: str

    content_type: str

    size: int = Field(
        ge=0,
    )

    storage_path: str

    checksum: str | None = None

    is_deleted: bool = False
