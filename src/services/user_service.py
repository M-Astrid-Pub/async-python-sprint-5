from infrastructure.repositories.user_repository import UserRepository
from models.dto.auth import UserCreate


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create(self, *, obj_in: UserCreate):
        return await self.user_repo.create(obj_in=obj_in)

    async def get(self, *, username: str):
        return await self.user_repo.get_by_username(username=username)

    async def has_access_to(self, *, username: str, path: str):
        return await self.user_repo.get_by_username(username=username)
