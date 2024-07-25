import uvicorn
from fastapi import FastAPI
from api import router
from core import settings

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
