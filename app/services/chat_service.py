from app.chat.conversation_builder import ConversationBuilder
from app.llm.factory import LLMFactory
from app.models.message import Message, Role


class ChatService:
    def __init__(self):
        self.llm = LLMFactory.create()
        self.conversation_builder = ConversationBuilder()

    def ask(self, message: str) -> str:
        conversation = self.conversation_builder.build(message)

        answer = self.llm.chat(conversation=conversation)

        conversation.add_assistant(answer)

        return answer
