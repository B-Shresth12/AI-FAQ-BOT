from app.chat.prompt_loader import PromptLoader
from app.models.conversation import Conversation


class ConversationBuilder:
    def __init__(self, prompt_name: str = "assistant"):
        self.prompt_name = prompt_name

    def build(self) -> Conversation:
        system_prompt = PromptLoader.load(self.prompt_name)

        conversation = Conversation()

        conversation.add_system(system_prompt)
        # conversation.add_user(user_message)
        
        return conversation
