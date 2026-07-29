from google import genai

from app.config.settings import settings
from app.llm.base import LLM
from app.models.message import Message


class GeminiService(LLM):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINII_API_KEY)

    # GEMINI Commuinicator
    def chat(self, message: list[Message]) -> str:
        contents = self.aggMessage(message=message)

        response = self.client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=contents,
        )

        return response.text
