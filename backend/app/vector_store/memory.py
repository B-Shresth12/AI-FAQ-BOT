import math

from app.config.settings import settings
from app.models.document_chunk import DocumentChunk
from app.vector_store.base import VectorStore


class MemoryVectorStore(VectorStore):
    def __init__(self):
        self._items = []

    def add(
        self,
        chunk: DocumentChunk,
        embedding: list[float],
    ) -> None:
        self._items.append((chunk, embedding))

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:
        results = []

        for chunk, stored_embedding in self._items:
            score = self._cosine_similarity(embedding, stored_embedding)
            if score >= settings.RAG_SIMILARITY_THRESHOLD:
                results.append((score, chunk))

        results.sort(key=lambda item: item[0], reverse=True)

        return [chunk for _, chunk in results[:limit]]

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:

        dot_product = sum(x * y for x, y in zip(a, b))

        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(x * x for x in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)
