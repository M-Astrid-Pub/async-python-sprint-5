from typing import List

from sqlalchemy import func, over, select

from infrastructure.db.engine import async_session
from models.dto.files import FileCreate, FileUpdate

from ..db.db_models import File as FileModel
from .base import ModelType, RepositoryDB


class FilesRepository(RepositoryDB[FileModel, FileCreate, FileUpdate]):
    async def get_multi_by_user(
        self, user_id: int, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = (
            select(
                self._model,
                over(func.count()).label("total"),
            )
            .where(self._model.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        async with self._session_maker() as db:
            results = await db.execute(statement=statement)
        return results.all()

    async def check_file_access(self, user_id: int, file_path: str):
        statement = (
            select(
                self._model,
                over(func.count()).label("total"),
            )
            .where(self._model.user_id == user_id)
            .where(self._model.path == file_path)
        )
        async with self._session_maker() as db:
            results = await db.execute(statement=statement)

        return bool(results.first())


files_repo = FilesRepository(FileModel, async_session)
