from google import genai

from app.config.settings import settings
from app.llm.base import LLM
from app.models.message import Message


class GeminiService(LLM):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINII_API_KEY)

    # GEMINI Commuinicator
    def chat(self, messages: list[Message]) -> str:
        contents = "\n\n".join(f"{msg.role.value}: {msg.content}" for msg in messages)

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
        )

        return response.text
