from abc import ABC, abstractmethod

from app.models.conversation import Conversation


class ConversationStore(ABC):
    @abstractmethod
    def get(self, conversation_id: str) -> Conversation | None:
        pass

    @abstractmethod
    def save(self, conversation_id: str, conversation: Conversation) -> None:
        pass
