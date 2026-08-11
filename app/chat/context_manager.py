from app.chat.token_counter import TokenCounter
from app.config.settings import settings
from app.models.conversation import Conversation
from app.models.message import Message, Role


class ContextManager:
    def __init__(self):
        self.token_counter = TokenCounter()

    # This build the conversation according the required request from user
    def build(self, conversation: Conversation) -> Conversation:
        if self.fits(conversation=conversation):
            return conversation

        context = Conversation()

        system_message = self._get_system_message(conversation)

        if system_message:
            context.add_message(system_message)

        messages = [
            message for message in conversation.messages if message.role != Role.SYSTEM
        ]

        for message in reversed(messages):
            context.add_message(message)

            if not self.fits(context):
                context.remove_message(-1)
                break

        context.messages.reverse()

        return context

    # Fetches system message
    def _get_system_message(self, conversation: Conversation) -> Message | None:
        for message in conversation.messages:
            if message.role == Role.SYSTEM:
                return message

        return None

    def fits(self, conversation: Conversation) -> bool:
        token_count = self.token_counter.count(conversation=conversation)

        return token_count <= settings.MAX_CONTEXT_TOKENS

    def trim(self, conversation: Conversation) -> Conversation:
        while not self.fits(conversation=conversation):
            removable_index = self._find_oldest_removable_message(conversation)

            if removable_index is None:
                break

            conversation.remove_message(removable_index)

        return conversation

    def _find_oldest_removable_message(self, conversation: Conversation) -> int | None:
        for index, message in enumerate(conversation.messages):
            if message.role != Role.SYSTEM:
                return index

        return None
