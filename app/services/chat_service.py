from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder
from app.chat.conversation_store import ConversationStore
from app.llm.base import LLM


class ChatService:
    def __init__(
        self,
        conversation_builder: ConversationBuilder,
        conversation_store: ConversationStore,
        context_manager: ContextManager,
        llm: LLM,
    ):
        self.llm = llm
        self.conversation_builder = conversation_builder
        self.conversation_store = conversation_store
        self.context_manager = context_manager

    def ask(self, conversation_id: str, message: str) -> str:
        conversation = self.conversation_store.get(conversation_id=conversation_id)

        if conversation is None:
            conversation = self.conversation_builder.build()

        conversation.add_user(message)
        self.context_manager.build(conversation=conversation)

        answer = self.llm.chat(conversation=conversation)

        conversation.add_assistant(answer)

        self.conversation_store.save(
            conversation_id=conversation_id, conversation=conversation
        )

        return answer
