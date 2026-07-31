import ollama

from app.config.settings import settings
from app.llm.base import LLM
from app.models.conversation import Conversation


class OllamaService(LLM):
    def _build_messages(self, conversation: Conversation):
        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in conversation.messages
        ]

    # Ollama Commuinicator
    def chat(self, conversation) -> str:

        result = ollama.chat(
            model=settings.OLLAMA_MODEL, messages=self._build_messages(conversation)
        )
        return result["message"].content
