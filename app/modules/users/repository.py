from app.infrastructure.database.base_repository import BaseRepository
from app.modules.users.models import UserDocument


class UserRepository(BaseRepository[UserDocument]):
    collection_name = "users"

    document_class = UserDocument


user_repository = UserRepository()
