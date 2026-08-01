from minio import Minio

from app.core.config import settings


class MinioStorage:
    """
    MinIO object storage client.
    """

    def __init__(self) -> None:
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

        self.bucket_name = settings.MINIO_BUCKET_NAME

    def ensure_bucket(self) -> None:
        """
        Create the storage bucket if it does not already exist.
        """

        if not self.client.bucket_exists(
            self.bucket_name,
        ):
            self.client.make_bucket(
                self.bucket_name,
            )


minio_storage = MinioStorage()
