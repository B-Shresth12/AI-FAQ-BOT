from app.chat.conversation_builder import ConversationBuilder
from app.llm.factory import LLMFactory
from app.models.message import Message, Role


class ChatService:
    def __init__(self):
        self.llm = LLMFactory.create()
        self.conversation_builder = ConversationBuilder()

    def ask(self, message: str) -> str:
        messages = self.conversation_builder.build(message)

        return self.llm.chat(messages=messages)
