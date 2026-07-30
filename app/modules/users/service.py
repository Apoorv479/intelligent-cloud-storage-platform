from app.modules.users.models import UserDocument
from app.modules.users.repository import user_repository
from app.modules.users.schemas import UserCreateRequest


class UserService:
    """
    User business logic.
    """

    async def create_user(
        self,
        request: UserCreateRequest,
    ) -> UserDocument:

        user = UserDocument(
            email=request.email,
            full_name=request.full_name,
        )

        return await user_repository.create(user)


user_service = UserService()
