from app.config.settings import settings
from app.llm.gemini import GeminiService
from app.llm.ollama import OllamaService


class LLMFactory:
    @staticmethod
    def create():
        if settings.LLM_PROVIDER == "gemini":
            return GeminiService()
        elif settings.LLM_PROVIDER == "ollama":
            return OllamaService()
        else:
            raise ValueError("Unsupported provider")
