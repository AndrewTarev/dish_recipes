from fastapi_users import schemas

from core.models.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
