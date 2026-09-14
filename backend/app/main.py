from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.config.settings import settings
from app.container import container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container.knowledge_initializer.initialize()

    yield


app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.include_router(chat_router)
