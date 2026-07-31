from pydantic import Field

from app.infrastructure.database.base_model import BaseDocument


class FolderDocument(BaseDocument):
    """
    MongoDB document representing a folder.
    """

    user_id: str

    parent_folder_id: str | None = None

    name: str = Field(
        min_length=1,
        max_length=255,
    )

    path: str

    is_deleted: bool = False
