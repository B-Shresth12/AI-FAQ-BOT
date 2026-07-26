from app.llm.gemini import GeminiService
from app.models.message import Message


class ChatService:
    def __init__(self):
        self.llm = GeminiService()

    def ask(self, message: list[Message]) -> str:
        return self.llm.chat(message=message)
