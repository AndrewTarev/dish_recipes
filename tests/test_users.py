# python -m pytest -v

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "nickname": "string",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v1/auth/login",
        json={
            "username": "user@example.com",
            "password": "string",
        },
    )
    assert response.status_code == 200
