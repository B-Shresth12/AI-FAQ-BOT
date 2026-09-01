from fastapi import APIRouter

from app.container import container
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = container.chat_service.ask(
        conversation_id=request.conversation_id, message=request.message
    )

    return ChatResponse(answer=answer)
