from abc import ABC, abstractmethod

from app.models.message import Message


class LLM(ABC):
    @abstractmethod
    def chat(self, message: list[Message]) -> str:
        pass
