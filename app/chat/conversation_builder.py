from app.chat.prompt_loader import PromptLoader
from app.models.message import Message, Role


class ConversationBuilder:
    def build(self, user_message: str) -> list[Message]:
        system_prompt = PromptLoader.load("assistant")

        return [
            Message(
                role=Role.SYSTEM, 
                content=system_prompt
            ),
            Message(
                role=Role.USER, 
                content=user_message
            ),
        ]
