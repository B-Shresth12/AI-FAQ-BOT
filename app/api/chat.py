from fastapi import APIRouter

from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder
from app.chat.conversation_store import ConversationStore
from app.embeddings.ollama import OllamaEmbedding
from app.llm.factory import LLMFactory
from app.models.chat import ChatRequest, ChatResponse
from app.rag.chunker import DocumentChunker
from app.rag.context_builder import RAGContextBuilder
from app.rag.indexer import KnowledgeIndexer
from app.rag.initializer import KnowledgeInitializer
from app.rag.knowledge_loader import KnowlegeLoader
from app.rag.retriever import Retriever
from app.services.chat_service import ChatService
from app.vector_store.memory import MemoryVectorStore

router = APIRouter()

embedding = OllamaEmbedding()
vector_store = MemoryVectorStore()
chunker = DocumentChunker()
indexer = KnowledgeIndexer(
    chunker=chunker, embedding=embedding, vector_store=vector_store
)

initializer = KnowledgeInitializer(
    loader=KnowlegeLoader(),
    indexer=indexer,
)

initializer.initialize()

chat_service = ChatService(
    conversation_builder=ConversationBuilder(),
    conversation_store=ConversationStore(),
    context_manager=ContextManager(),
    llm=LLMFactory.create(),
    retriever=Retriever(embedding=embedding, vector_store=vector_store),
    rag_context_builder=RAGContextBuilder,
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = chat_service.ask(
        conversation_id=request.conversation_id, message=request.message
    )

    return ChatResponse(answer=answer)
