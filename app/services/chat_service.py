from app.llm.gemini import GeminiService
from app.models.message import Message, Role
from app.prompts.loader import PromptLoader


class ChatService:
    def __init__(self):
        self.llm = GeminiService()

    def ask(self, message: list[Message]) -> str:
        system_prompt = PromptLoader.load("assistant")

        messages = [
            Message(
                role=Role.SYSTEM,
                content=system_prompt,
            ),
            Message(
                role=Role.USER,
                content=message,
            ),
        ]
        return self.llm.chat(message=messages)
