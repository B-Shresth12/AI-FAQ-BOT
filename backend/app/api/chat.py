from fastapi import APIRouter

from app.container import container
from app.models.chat import ChatRequest, ChatResponse
from app.models.message import Role

router = APIRouter()


@router.get("/get-conversations")
def getConversations():
    conversations = container.conversation_store.get_conversations()

    return {
        "conversations": [
            {
                "id": conversation.id,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
            }
            for conversation in conversations
        ]
    }


@router.get("/get-message")
def getMessage(conversation_id: str):
    conversation = container.conversation_store.get(conversation_id=conversation_id)

    if conversation is None:
        return {"message": []}

    return {
        "messages": [
            {"role": message.role.value, "content": message.content}
            for message in conversation.messages
            if message.role != Role.SYSTEM and message.role != Role.CONTEXT
        ]
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = container.chat_service.ask(
        conversation_id=request.conversation_id, message=request.message
    )

    return ChatResponse(answer=answer)
