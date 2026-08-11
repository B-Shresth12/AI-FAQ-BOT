from transformers import AutoTokenizer

from app.config.settings import Settings
from app.models.conversation import Conversation


class TokenCounter:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(Settings.TOKENIZER_MODEL)

    def count(self, conversation: Conversation) -> int:
        text = "\n\n".join(
            f"{message.role.value}: {message.content}"
            for message in conversation.messages
        )

        return len(self.tokenizer.encode(text))
