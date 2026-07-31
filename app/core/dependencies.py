from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.modules.users.models import UserDocument
from app.modules.users.repository import user_repository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> UserDocument:
    """
    Retrieve the authenticated user from a JWT access token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationException("Invalid authentication token.")

    except JWTError:
        raise AuthenticationException("Invalid authentication token.")

    user = await user_repository.get_by_id(user_id)
    print("User loaded:", user)

    if user is None:
        raise AuthenticationException("User not found.")

    if not user.is_active:
        raise AuthenticationException("Account is inactive.")

    return user
