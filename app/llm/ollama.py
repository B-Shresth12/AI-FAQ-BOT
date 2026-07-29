import ollama

from app.config.settings import settings
from app.llm.base import LLM


class OllamaService(LLM):
    def chat(self, message) -> str:
        contents = self.aggMessage(message=message)

        result = ollama.generate(model=settings.MODEL_NAME, prompt=contents)
        return result["response"]
