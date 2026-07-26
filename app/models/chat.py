from pydantic import BaseModel

from app.models.message import Message


class ChatRequest(BaseModel):
    message: list[Message]


class ChatResponse(BaseModel):
    answer: str
