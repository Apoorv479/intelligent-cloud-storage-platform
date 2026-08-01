from app.infrastructure.database.base_repository import BaseRepository
from app.modules.files.models import FileDocument


class FileRepository(BaseRepository[FileDocument]):
    """
    File repository.
    """

    collection_name = "files"

    document_class = FileDocument


file_repository = FileRepository()
