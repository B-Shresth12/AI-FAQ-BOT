from abc import ABC, abstractmethod

from app.models.conversation import Conversation


class LLM(ABC):
    @abstractmethod
    def chat(self, conversation: Conversation) -> str:
        pass
