from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.config.settings import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.include_router(chat_router)
