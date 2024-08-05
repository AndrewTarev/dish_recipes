# python -m pytest -v

from httpx import AsyncClient
import pytest

from fastapi_application.actions.create_superuser import create_superuser
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
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_logout_user(ac: AsyncClient) -> None:
    response = await ac.post("/api/v1/auth/logout")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_superuser(ac: AsyncClient) -> None:
    await create_superuser(async_session)


# @pytest.mark.asyncio
# async def test_create_dishes(ac: AsyncClient) -> None:
#     response = await ac.post(
#         "/api/v1/auth/create_dishes",
#     )
