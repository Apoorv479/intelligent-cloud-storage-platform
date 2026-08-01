from io import BytesIO

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

    def upload_file(
        self,
        object_name: str,
        data: bytes,
        content_type: str,
    ) -> None:
        """
        Upload a file to MinIO.
        """

        stream = BytesIO(data)

        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=stream,
            length=len(data),
            content_type=content_type,
        )

    def delete_file(
        self,
        object_name: str,
    ) -> None:
        """
        Delete a file from MinIO.
        """

        self.client.remove_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
        )


minio_storage = MinioStorage()
