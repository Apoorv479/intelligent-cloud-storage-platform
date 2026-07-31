from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from app.core.config import settings

# JWT Configuration


SECRET_KEY = "..."

ALGORITHM = "..."

ACCESS_TOKEN_EXPIRE_MINUTES = ...

REFRESH_TOKEN_EXPIRE_DAYS = ...


# Password Hashing


def hash_password(
    password: str,
) -> str:
    """
    Hash a plaintext password.
    """

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    )

    return hashed.decode()


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password.
    """

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )


# JWT Creation


def create_access_token(
    subject: str,
) -> str:
    """
    Create a JWT access token.
    """

    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(
    subject: str,
    version: int,
) -> str:
    """
    Create a JWT refresh token.
    """

    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
        "version": version,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_refresh_token(
    token: str,
) -> dict:
    """
    Verify and decode a refresh token.
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    if payload.get("type") != "refresh":
        raise JWTError("Invalid refresh token.")

    return payload
