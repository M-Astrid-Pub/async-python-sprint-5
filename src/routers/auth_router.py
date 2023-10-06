import inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from models.dto.auth import TokenResponse, UserCreate
from services.user_service import UserService
from utils.jwt_helper import access_security
from utils.password_checker import verify_password

router = APIRouter()


async def get_user_service() -> UserService:
    return inject.instance(UserService)


@router.post("/signup")
async def signup(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    user_id = await service.create(obj_in=user)
    subject = {"id": user_id, "username": user.username}
    access_token = access_security.create_access_token(
        subject=subject,
    )
    return ORJSONResponse(
        status_code=201,
        content=TokenResponse(access_token=access_token, user_id=user_id),
    )


@router.post("/login")
async def login(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    user_db = await service.get(username=user.username)

    if not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = access_security.create_access_token(
        subject={"id": user_db.id, "username": user_db.username}
    )
    return ORJSONResponse(
        status_code=201,
        content=TokenResponse(access_token=access_token, user_id=user_db.id),
    )
