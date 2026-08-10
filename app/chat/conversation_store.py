from app.models.conversation import Conversation


class ConversationStore:
    def __init__(self):
        self._conversations: dict[str, Conversation] = {}

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def save(self, conversation_id: str, conversation: Conversation) -> None:
        self._conversations[conversation_id] = conversation
