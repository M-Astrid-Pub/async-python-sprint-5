from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_TEST_DB: str
    S3_BUCKET_NAME: str

    BLACKLIST: list[str] = []
    APP_LOG_LEVEL: str = "INFO"
    ENABLE_LOG_FORMATTER: bool = True

    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=12)

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str

    class Config:
        env_file = ".env"

    def get_pg_url(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


app_settings = Settings()
