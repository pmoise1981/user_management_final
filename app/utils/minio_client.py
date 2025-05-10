from minio import Minio
from minio.error import S3Error
from app.dependencies import get_settings
from pathlib import Path

settings = get_settings()

# Initialize MinIO client
minio_client = Minio(
    endpoint=settings.minio_endpoint.replace("http://", "").replace("https://", ""),
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_endpoint.startswith("https"),
)


def upload_qr_to_minio(file_path: Path, object_name: str) -> str:
    """
    Uploads a local QR code image to MinIO and returns its public URL.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"QR code file not found: {file_path}")

    # Ensure bucket exists *before* uploading
    try:
        if not minio_client.bucket_exists(settings.minio_bucket_name):
            minio_client.make_bucket(settings.minio_bucket_name)
    except S3Error as e:
        raise RuntimeError(f"MinIO error while checking/creating bucket: {e}")

    # Upload QR code
    minio_client.fput_object(
        bucket_name=settings.minio_bucket_name,
        object_name=object_name,
        file_path=str(file_path),
        content_type="image/png"
    )

    return f"{settings.minio_endpoint}/{settings.minio_bucket_name}/{object_name}"

