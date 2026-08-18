from abc import ABC, abstractmethod

from app.models.document_chunk import DocumentChunk


class VectorStore(ABC):
    @abstractmethod
    def add(self, chunk: DocumentChunk, embedding: list[float]) -> None:
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:
        pass
