from abc import ABC, abstractmethod


class Embedding(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass
