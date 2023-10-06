import time

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.engine import get_session
from utils.jwt_helper import access_security, credentials_exception

system_router = APIRouter(tags=["System"])


@system_router.get("/healthz")
async def health() -> dict[str, bool]:
    return {"ok": True}


@system_router.get("/readyz")
async def ready() -> dict[str, bool]:
    return {"ok": True}


@system_router.get("/ping")
async def ping(
    db: AsyncSession = Depends(get_session),
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> dict[str, bool]:
    if not credentials:
        raise credentials_exception

    start = time.time()
    await db.connection()
    db_ping = time.time() - start
    return {"ok": True, "db_ping": db_ping}
