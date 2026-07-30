from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt

# JWT Configuration


SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 7


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

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(
    subject: str,
    version: int,
) -> str:
    """
    Create a JWT refresh token.
    """

    expire = datetime.now(UTC) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS,
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
        "version": version,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
