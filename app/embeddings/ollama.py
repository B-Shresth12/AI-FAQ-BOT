import ollama

from app.config.settings import settings
from app.embeddings.base import Embedding


class OllamaEmbedding(Embedding):
    def embed(self, text: str) -> list[float]:
        response = ollama.embed(model=settings.EMBEDDING_MODEL, input=text)

        return response["embeddings"][0]
