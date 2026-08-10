from app.chat.token_counter import TokenCounter
from app.config.settings import settings
from app.models.conversation import Conversation


class ContextManager:
    def __init__(self):
        self.token_counter = TokenCounter("Qwen/Qwen3-8B")

    def fits(self, conversation: Conversation) -> bool:
        token_count = self.token_counter.count(conversation=conversation)

        return token_count <= settings.MAX_CONTEXT_TOKENS
