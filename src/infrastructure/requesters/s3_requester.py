import aioboto3

from settings import app_settings


class S3Requester:
    def __init__(self):
        self.s3 = aioboto3.Session().client(
            service_name="s3",
            endpoint_url="https://storage.yandexcloud.net",
            aws_access_key_id=app_settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=app_settings.AWS_SECRET_ACCESS_KEY,
        )

    async def upload_file(self, temp_file_path: str, file_path: str):
        await self.s3.upload_file(
            temp_file_path, app_settings.S3_BUCKET_NAME, file_path
        )
