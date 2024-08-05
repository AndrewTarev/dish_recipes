from fastapi_users import FastAPIUsers

from fastapi_application.api.dependencies.authentication.backend import (
    authentication_backend,
)
from fastapi_application.api.dependencies.authentication.user_manager import (
    get_user_manager,
)
from fastapi_application.core.models import User
from fastapi_application.core.models.types.user_id import UserIdType


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
