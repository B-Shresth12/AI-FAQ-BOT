from transformers import AutoTokenizer

from app.models.conversation import Conversation


class TokenCounter:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def count(self, conversation: Conversation) -> int:
        text = "\n\n".join(
            f"{message.role.value}: {message.content}"
            for message in conversation.messages
        )

        return len(self.tokenizer.encode(text))
