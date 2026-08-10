from fastapi import APIRouter

from app.chat.conversation_builder import ConversationBuilder
from app.chat.conversation_store import ConversationStore
from app.llm.factory import LLMFactory
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService(
    conversation_builder=ConversationBuilder(),
    conversation_store=ConversationStore(),
    llm=LLMFactory.create(),
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = chat_service.ask(
        conversation_id=request.conversation_id, message=request.message
    )

    return ChatResponse(answer=answer)


# chamal
# rato tika
# pahilo tika
# chiura
# sano kerau
# jerry - X
# chanchun paisa
