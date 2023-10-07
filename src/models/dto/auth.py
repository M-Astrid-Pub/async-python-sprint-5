from dataclasses import dataclass

from pydantic import BaseModel, Field

from infrastructure.db.db_models import User as UserDB
from utils.password_checker import pwd_context


class UserCreate(BaseModel):
    username: str
    password: str = Field(max_length=55)

    @property
    def hashed_password(self) -> str:
        return pwd_context.hash(self.password)

    async def to_db_model(self):
        return UserDB(
            username=self.username,
            hashed_password=self.hashed_password,
        )


@dataclass
class TokenResponse:
    access_token: str
    user_id: int
