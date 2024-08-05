from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.actions.create_superuser import create_superuser
from src.api import router
from src.core import settings
from src.core.models import db_helper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # connect to Redis
    redis = aioredis.from_url(settings.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # create superuser
    await create_superuser(db_helper.session_factory)
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
