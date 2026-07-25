import boto3
from pathlib import Path
from datetime import datetime

BUCKET_NAME = "moksha-arcgis-validator"

s3 = boto3.client("s3")


def upload_file(file_path):
    """
    Upload a file to S3 inside a timestamped run folder.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    run_folder = datetime.now().strftime("runs/%Y-%m-%d_%H-%M-%S")

    object_key = f"{run_folder}/{file_path.name}"

    s3.upload_file(
        str(file_path),
        BUCKET_NAME,
        object_key
    )

    print(f"Uploaded {file_path.name}")

    print(f"s3://{BUCKET_NAME}/{object_key}")