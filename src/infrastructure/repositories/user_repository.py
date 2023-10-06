from sqlalchemy import select

from exceptions import ObjectNotFoundException
from infrastructure.db.db_models import User as UserModel
from infrastructure.db.engine import async_session
from models.dto.auth import UserCreate

from .base import RepositoryDB


class UserRepository(RepositoryDB[UserModel, UserCreate, UserCreate]):
    async def get_by_username(self, username: str) -> UserModel:
        statement = select(self._model).where(self._model.username == username)
        async with self._session_maker() as db:
            results = await db.execute(statement=statement)
        if not (res := results.scalar_one_or_none()):
            raise ObjectNotFoundException
        return res

    async def create(self, *, obj_in: UserCreate) -> UserModel:
        db_obj = await obj_in.to_db_model()
        async with self._session_maker() as db:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj.id


user_repo = UserRepository(UserModel, async_session)
