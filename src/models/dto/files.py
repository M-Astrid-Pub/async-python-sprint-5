from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, Field


class FileCreate(BaseModel):
    path: str = Field(max_length=256)
    size: int
    is_downloadable: bool
    name: str = Field(max_length=64)
    user_id: int


class FileUpdate(FileCreate):
    pass


@dataclass
class FileResponse:
    path: str
    size: int
    is_downloadable: bool
    id: int
    name: str
    created_at: datetime

    @classmethod
    def from_entity(cls, file):
        return cls(
            path=file.path,
            size=file.size,
            is_downloadable=file.is_downloadable,
            id=file.id,
            name=file.name,
            created_at=file.created_at,
        )


@dataclass
class MultipleFilesResponse:
    user_id: int
    files: list[FileResponse]
    total: int

    @classmethod
    def from_entity_list(cls, user_id, rows):
        if len(rows) == 0:
            return cls(user_id=user_id, total=0, files=[])

        return cls(
            user_id=user_id,
            total=rows[0][1],
            files=[FileResponse.from_entity(row[0]) for row in rows],
        )
