import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.db import File
from infrastructure.db.base import metadata
from infrastructure.repositories.files_repository import FilesRepository
from infrastructure.repositories.user_repository import user_repo
from infrastructure.requesters.s3_requester import S3Requester
from main import app
from models.dto.auth import TokenResponse, UserCreate
from models.dto.files import FileCreate
from routers.auth_router import get_user_service
from routers.files_router import get_files_service
from services.files_service import FilesService
from services.user_service import UserService
from settings import app_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


app_settings.PG_DB = app_settings.PG_TEST_DB
engine_test = create_async_engine(app_settings.get_pg_url(), future=True)
async_session = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


@pytest.fixture(scope="session")
async def prepare_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="module")
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_dummy_s3() -> S3Requester:
    s3 = S3Requester()
    s3.upload_file = AsyncMock(return_value=None)
    return s3


async def get_dummy_service() -> FilesService:
    return FilesService(await get_dummy_s3())


async def get_dummy_user_service() -> UserService:
    return UserService(user_repo)


app.dependency_overrides[get_files_service] = get_dummy_service
app.dependency_overrides[get_user_service] = get_dummy_user_service


@pytest.fixture(scope="module")
async def dummy_file_create() -> FileCreate:
    return FileCreate(
        path="test.txt",
    )


@pytest.fixture(scope="session")
async def dummy_user() -> UserCreate:
    return UserCreate(username="test", password="test")


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authed_client(
    client: httpx.AsyncClient, dummy_user: UserCreate, prepare_db
) -> httpx.AsyncClient:
    result = await client.post(
        app.url_path_for("signup"), json=jsonable_encoder(dummy_user)
    )
    client.headers = {
        "Authorization": f"Bearer {result.json()['access_token']}"
    }
    return client
