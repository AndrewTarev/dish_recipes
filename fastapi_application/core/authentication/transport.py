from fastapi_users.authentication import BearerTransport

from fastapi_application.core import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)
