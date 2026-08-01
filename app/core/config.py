from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.

    All configuration values are loaded from the .env file.
    """

    APP_NAME: str = "Intelligent Cloud Storage Platform"
    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # MongoDB

    MONGODB_URI: str
    MONGODB_DATABASE: str

    MINIO_ENDPOINT: str = "localhost:9000"

    MINIO_ACCESS_KEY: str = "minioadmin"

    MINIO_SECRET_KEY: str = "minioadmin123"

    MINIO_BUCKET_NAME: str = "cloud-storage"

    MINIO_SECURE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()


settings = get_settings()
