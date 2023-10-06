from typing import Generic, Type, TypeVar

from infrastructure.repositories.base import (CreateSchemaType, RepositoryDB,
                                              UpdateSchemaType)


class Service:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_list(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


RepositoryType = TypeVar("RepositoryType", bound=RepositoryDB)


class BaseService(
    Service, Generic[RepositoryType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, repo: Type[RepositoryType]):
        self._repo = repo

    async def get(self, obj_id):
        return await self._repo.get(id=obj_id)

    async def get_list(self, user, limit, offset):
        return await self._repo.get_multi(limit=limit, offset=offset)

    async def create(self, obj_data: CreateSchemaType):
        return await self._repo.create(obj_in=obj_data)

    async def update(self, obj_id: int, obj_data: UpdateSchemaType):
        return await self._repo.update(obj_id=obj_id, obj_in=obj_data)

    async def delete(self, obj_id: int):
        return await self._repo.delete(obj_id=obj_id)
