# python -m pytest -v
from os import getenv

from httpx import AsyncClient
import pytest

from tests.conftest import async_session
from tests.settings_test import UserTest, login_credentials_schema


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": UserTest.EMAIL,
            "password": UserTest.PASSWORD,
            "nickname": UserTest.NICKNAME,
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/auth/login",
        data=login_credentials_schema,
    )
    assert response.json().get("access_token") is not None
    assert response.json().get("token_type") == "bearer"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_request_verify_token_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/auth/request-verify-token",
        json={"email": UserTest.EMAIL},
    )
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_create_superuser(ac: AsyncClient) -> None:
    superuser = await create_superuser(async_session)
    assert superuser.email == getenv("DEFAULT_EMAIL")
    assert superuser.is_superuser is True


@pytest.mark.asyncio
async def test_reset_password_token(
    ac: AsyncClient,
) -> None:
    login = await ac.post("/api/v1/auth/forgot-password", json=UserTest.EMAIL)
    login_token = login.headers.get("Authorization")
    if not login_token:
        # Если токен в заголовках отсутствует, проверяем тело ответа
        login_json = login.json()
        login_token = login_json.get("token")

    response = await ac.post(
        "/api/v1/auth/reset-password",
        json={
            "token": login_token,
            "password": UserTest.NEW_PASSWORD,
        },
    )
    assert response.status_code == 200
