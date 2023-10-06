import os

from fastapi import UploadFile

from infrastructure.repositories.files_repository import files_repo
from infrastructure.requesters.s3_requester import S3Requester
from models.dto.files import FileCreate
from services.base import BaseService


class FilesService(BaseService):
    def __init__(self, s3: S3Requester):
        super().__init__(files_repo)
        self.s3 = s3

    async def get_list(self, user_id: int, limit: int, offset: int):
        return await self._repo.get_multi_by_user(
            user_id=user_id, limit=limit, offset=offset
        )

    async def upload_file(self, user_id: int, path: str, file: UploadFile):
        target_path = os.path.join(str(user_id), path)
        if not os.path.splitext(target_path)[1]:
            target_path = os.path.join(target_path, file.filename)

        tmp_local_path = os.path.join("tmp", str(user_id), target_path)
        tmp_local_path_dir = os.path.dirname(tmp_local_path)
        if not os.path.exists(tmp_local_path_dir):
            os.makedirs(tmp_local_path_dir)

        contents = await file.read()
        with open(tmp_local_path, "wb") as f:
            f.write(contents)
        try:
            await self.s3.upload_file(tmp_local_path, target_path)
        except Exception:
            os.remove(tmp_local_path)
            raise

        file_obj = await self._repo.create(
            obj_in=FileCreate(
                path=path,
                user_id=user_id,
                size=file.size,
                is_downloadable=True,
                name=file.filename,
            )
        )

        os.remove(tmp_local_path)
        return file_obj

    async def check_file_access(self, user_id: int, file_path: str):
        return await self._repo.check_file_access(user_id, file_path)
