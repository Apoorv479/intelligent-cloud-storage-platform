from pydantic import BaseModel, ConfigDict, Field


class FolderCreateRequest(BaseModel):
    """
    Request schema for creating a folder.
    """

    parent_folder_id: str | None = None

    name: str = Field(
        min_length=1,
        max_length=255,
    )


class FolderUpdateRequest(BaseModel):
    """
    Request schema for renaming a folder.
    """

    name: str = Field(
        min_length=1,
        max_length=255,
    )


class FolderResponse(BaseModel):
    """
    Folder response schema.
    """

    id: str

    user_id: str

    parent_folder_id: str | None

    name: str

    path: str

    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
