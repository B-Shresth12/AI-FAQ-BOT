from google import genai

from app.config.settings import settings


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINII_API_KEY)

    # GEMINI Commuinicator
    def chat(self, message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-3.5-flash", contents=message
        )

        return response.text
