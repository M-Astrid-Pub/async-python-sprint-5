import boto3

from settings import app_settings


class S3Requester:
    def __init__(self):
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name="s3", endpoint_url="https://storage.yandexcloud.net"
        )

    async def upload_file(self, temp_file_path: str, file_path: str):
        self.s3.upload_file(
            temp_file_path, app_settings.S3_BUCKET_NAME, file_path
        )
