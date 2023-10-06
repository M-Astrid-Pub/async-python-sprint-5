import logging

import inject
from fastapi import FastAPI

from infrastructure.db.engine import engine
from infrastructure.repositories.files_repository import files_repo
from infrastructure.repositories.user_repository import user_repo
from middleware.ip_block_middleware import BlacklistMiddleware
from routers.auth_router import router as auth_router
from routers.files_router import exceptions_map as file_exceptions
from routers.files_router import router as file_router
from services.files_service import FilesService
from services.user_service import UserService
from settings import app_settings
from utils.logger import log_handler

logging.basicConfig(handlers=[log_handler], level=app_settings.APP_LOG_LEVEL)


# Инициализация объекта приложения
app = FastAPI()
app.include_router(file_router)
app.include_router(auth_router)

# Обработчики исключений
for exc, response in file_exceptions.items():
    app.add_exception_handler(exc, lambda req, _: response.to_orjson())

# Прослойка для бана по ip
app.add_middleware(BlacklistMiddleware, blacklist=app_settings.BLACKLIST)

# Инициализация сервисов
user_service = UserService(user_repo)
service = FilesService(files_repo)


def config(binder: inject.Binder) -> None:
    binder.bind(UserService, user_service)
    binder.bind(FilesService, service)


@app.on_event("startup")
async def startup_event():
    inject.configure(config, bind_in_runtime=False)


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down...")
    await engine.dispose()
