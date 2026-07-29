from abc import ABC, abstractmethod

from app.models.message import Message


class LLM(ABC):
    @abstractmethod
    def chat(self, message: list[Message]) -> str:
        pass

    def aggMessage(self, message: list[Message]) -> str:
        return "\n\n".join(f"{msg.role.value}: {msg.content}" for msg in message)
