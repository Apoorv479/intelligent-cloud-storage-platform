from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    """
    Response schema for a stored file.
    """

    id: str

    user_id: str

    folder_id: str | None

    original_name: str

    storage_name: str

    content_type: str

    size: int

    storage_path: str

    checksum: str | None

    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
