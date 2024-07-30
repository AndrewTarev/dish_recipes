from fastapi_users import schemas

from core.models.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    nickname: str


class UserCreate(schemas.BaseUserCreate):
    nickname: str


class UserUpdate(schemas.BaseUserUpdate):
    nickname: str = None
