from app.infrastructure.database.base_repository import BaseRepository
from app.modules.folders.models import FolderDocument


class FolderRepository(BaseRepository[FolderDocument]):
    """
    Folder repository.
    """

    collection_name = "folders"

    document_class = FolderDocument


folder_repository = FolderRepository()
