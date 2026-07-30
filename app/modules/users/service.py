from app.core.exceptions import ConflictException, NotFoundException
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

        existing_user = await user_repository.get_one(
            {
                "email": request.email,
            }
        )

        if existing_user is not None:
            raise ConflictException("Email already exists.")

        user = UserDocument(
            email=request.email,
            full_name=request.full_name,
        )

        return await user_repository.create(user)

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> UserDocument:
        """
        Retrieve a user by id.
        """

        user = await user_repository.get_by_id(user_id)

        if user is None:
            raise NotFoundException("User not found.")

        return user


user_service = UserService()
