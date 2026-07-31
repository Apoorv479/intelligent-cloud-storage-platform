from app.core.exceptions import ConflictException
from app.core.security import hash_password
from app.modules.users.models import UserDocument
from app.modules.users.repository import user_repository
from app.modules.users.schemas import UserRegisterRequest
from datetime import UTC, datetime

from app.core.exceptions import (
    AuthenticationException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_refresh_token,
)
from app.modules.users.schemas import (
    TokenResponse,
    UserLoginRequest,
)


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

    async def login(
        self,
        request: UserLoginRequest,
    ) -> TokenResponse:
        """
        Authenticate a user.
        """

        user = await user_repository.get_one(
            {
                "email": request.email,
            }
        )

        if user is None:
            raise AuthenticationException("Invalid email or password.")

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise AuthenticationException("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationException("Account is inactive.")

        await user_repository.update(
            user.id,
            {
                "last_login": datetime.now(UTC),
            },
        )

        access_token = create_access_token(
            subject=user.id,
        )

        refresh_token = create_refresh_token(
            subject=user.id,
            version=user.refresh_token_version,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(
        self,
        refresh_token: str,
    ) -> TokenResponse:
        """
        Refresh an access token using a refresh token.
        """

        try:
            payload = verify_refresh_token(
                refresh_token,
            )

        except Exception:
            raise AuthenticationException("Invalid refresh token.")

        user_id = payload.get("sub")
        token_version = payload.get("version")

        if user_id is None:
            raise AuthenticationException("Invalid refresh token.")

        user = await user_repository.get_by_id(user_id)

        if user is None:
            raise AuthenticationException("User not found.")

        if not user.is_active:
            raise AuthenticationException("Account is inactive.")

        if token_version != user.refresh_token_version:
            raise AuthenticationException("Refresh token has been revoked.")

        access_token = create_access_token(
            subject=user.id,
        )

        new_refresh_token = create_refresh_token(
            subject=user.id,
            version=user.refresh_token_version,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )


auth_service = AuthService()
