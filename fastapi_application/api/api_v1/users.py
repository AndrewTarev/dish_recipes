from fastapi import APIRouter

from fastapi_application.api.api_v1.fastapi_users import fastapi_users
from fastapi_application.core.config import settings
from fastapi_application.core.schemas.user import (
    UserRead,
    UserUpdate,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
