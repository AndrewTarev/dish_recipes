import asyncio
import contextlib
from os import getenv

from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy.ext.asyncio import async_sessionmaker

from fastapi_application.api.dependencies.authentication import get_users_db
from fastapi_application.api.dependencies.authentication import get_user_manager
from fastapi_application.core.authentication.user_manager import UserManager
from fastapi_application.core.models import (
    db_helper,
    User,
)

from fastapi_application.core.schemas.user import UserCreate

# get_async_session_context = contextlib.asynccontextmanager(db_helper.session_getter())
get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = getenv("DEFAULT_EMAIL", "admin@admin.com")
default_password = getenv("DEFAULT_PASSWORD", "abc")
default_nickname = getenv("DEFAULT_NICKNAME", "superuser")
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    db_sessionmaker: async_sessionmaker,
    email: str = default_email,
    password: str = default_password,
    nickname: str = default_nickname,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        nickname=nickname,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    try:
        async with db_sessionmaker() as session:
            async with get_users_db_context(session) as users_db:
                async with get_user_manager_context(users_db) as user_manager:
                    return await create_user(
                        user_manager=user_manager,
                        user_create=user_create,
                    )
    except UserAlreadyExists:
        print("Superuser already exists")


if __name__ == "__main__":
    asyncio.run(create_superuser())
