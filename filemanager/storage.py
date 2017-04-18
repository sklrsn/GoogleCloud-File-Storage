from google.cloud import storage
import os

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
gcs = storage.Client()


def store_file(file):
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    return blob.public_url
