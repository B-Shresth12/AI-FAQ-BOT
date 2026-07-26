from fastapi import APIRouter

from app.llm.gemini import GeminiService
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()

gemini = GeminiService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = gemini.chat(request.message)

    return ChatResponse(answer=answer)
