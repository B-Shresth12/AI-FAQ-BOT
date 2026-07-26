from google import genai

from app.config.settings import settings
from app.llm.base import LLM
from app.models.message import Message


class GeminiService(LLM):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINII_API_KEY)

    # GEMINI Commuinicator
    def chat(self, message: list[Message]) -> str:
        response = self.client.models.generate_content(
            model="gemini-3.5-flash", contents=message[0].content
        )

        return response.text
