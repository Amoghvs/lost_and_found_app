from fastapi import UploadFile
from minio import Minio
from uuid import uuid4

minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

BUCKET_NAME = "lostfound"



def upload_to_minio(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    object_name = f"images/{uuid4()}.{ext}"

    # IMPORTANT: use file.file (a SpooledTemporaryFile), not file.file.read()
    file.file.seek(0, 2)  # Move to end to get size
    size = file.file.tell()
    file.file.seek(0)     # Reset pointer to beginning

    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

    minio_client.put_object(
        BUCKET_NAME,
        object_name,
        data=file.file,
        length=size,
        content_type=file.content_type,
    )

    return f"http://localhost:9000/{BUCKET_NAME}/{object_name}"
