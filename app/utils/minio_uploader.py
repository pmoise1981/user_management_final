from minio import Minio
from minio.error import S3Error
from pathlib import Path
import os

from app.dependencies import get_settings

settings = get_settings()

# Initialize the MinIO client
minio_client = Minio(
    endpoint=settings.minio_endpoint.replace("http://", "").replace("https://", ""),
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_endpoint.startswith("https://"),
)

def upload_qr_code_to_minio(local_path: str, object_name: str) -> str:
    """
    Uploads a local QR code image to the configured MinIO bucket and returns the public URL.
    """
    try:
        # Create bucket if it doesn't exist
        if not minio_client.bucket_exists(settings.minio_bucket_name):
            minio_client.make_bucket(settings.minio_bucket_name)

        # Upload the file
        minio_client.fput_object(
            bucket_name=settings.minio_bucket_name,
            object_name=object_name,
            file_path=local_path,
        )

        # Return public URL format
        return f"{settings.minio_endpoint}/{settings.minio_bucket_name}/{object_name}"
    except S3Error as e:
        raise RuntimeError(f"MinIO upload failed: {e}")

