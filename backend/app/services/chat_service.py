from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder
from app.chat.conversation_store import ConversationStore
from app.llm.base import LLM
from app.rag.context_builder import RAGContextBuilder
from app.rag.retriever import Retriever


class ChatService:
    def __init__(
        self,
        conversation_builder: ConversationBuilder,
        conversation_store: ConversationStore,
        context_manager: ContextManager,
        llm: LLM,
        retriever: Retriever,
        rag_context_builder: RAGContextBuilder,
    ):
        self.llm = llm
        self.conversation_builder = conversation_builder
        self.conversation_store = conversation_store
        self.context_manager = context_manager
        self.retriever = retriever
        self.rag_context_builder = rag_context_builder

    def ask(self, conversation_id: str, message: str) -> str:
        conversation = self.conversation_store.get(conversation_id=conversation_id)

        if conversation is None:
            conversation = self.conversation_builder.build()

        conversation.add_user(message)

        chunks = self.retriever.retrieve(
            query=message,
        )
        context = self.rag_context_builder.build(
            conversation=conversation, chunks=chunks
        )

        context = self.context_manager.build(conversation=context)

        answer = self.llm.chat(conversation=context)

        conversation.add_assistant(answer)

        self.conversation_store.save(
            conversation_id=conversation_id, conversation=conversation
        )

        return answer
