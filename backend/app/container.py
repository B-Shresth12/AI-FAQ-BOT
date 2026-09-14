from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder
from app.chat.conversation_store import ConversationStore
from app.embeddings.ollama import OllamaEmbedding
from app.llm.factory import LLMFactory
from app.rag.chunker import DocumentChunker
from app.rag.context_builder import RAGContextBuilder
from app.rag.indexer import KnowledgeIndexer
from app.rag.initializer import KnowledgeInitializer
from app.rag.knowledge_loader import KnowlegeLoader
from app.rag.retriever import Retriever
from app.services.chat_service import ChatService
from app.vector_store.chroma import ChromaVectorStore


class Container:
    def __init__(self):
        # Infrastructure
        self.embedding = OllamaEmbedding()
        self.vector_store = ChromaVectorStore()

        # Knowledge / RAG
        self.chunker = DocumentChunker()

        self.indexer = KnowledgeIndexer(
            chunker=self.chunker,
            embedding=self.embedding,
            vector_store=self.vector_store,
        )

        self.knowledge_initializer = KnowledgeInitializer(
            loader=KnowlegeLoader(),
            indexer=self.indexer,
        )

        self.retriever = Retriever(
            embedding=self.embedding, vector_store=self.vector_store
        )

        self.rag_context_builder = RAGContextBuilder()

        # Conversation
        self.conversation_builder = ConversationBuilder()
        self.conversation_store = ConversationStore()
        self.context_manager = ContextManager()

        self.llm = LLMFactory.create()

        # self.initializer.initialize()

        self.chat_service = ChatService(
            conversation_builder=self.conversation_builder,
            conversation_store=self.conversation_store,
            context_manager=self.context_manager,
            llm=self.llm,
            retriever=self.retriever,
            rag_context_builder=self.rag_context_builder,
        )


container = Container()
# container.knowledge_initializer.initialize()
