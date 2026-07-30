from app.core.exceptions import ConflictException
from app.core.security import hash_password
from app.modules.users.models import UserDocument
from app.modules.users.repository import user_repository
from app.modules.users.schemas import UserRegisterRequest


class AuthService:
    """
    Authentication business logic.
    """

    async def register(
        self,
        request: UserRegisterRequest,
    ) -> UserDocument:
        """
        Register a new user.
        """

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
            hashed_password=hash_password(request.password),
        )

        return await user_repository.create(user)


auth_service = AuthService()
