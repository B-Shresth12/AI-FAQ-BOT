from app.models.message import Message, Role


class Conversation:
    def __init__(self):
        self._messages: list[Message] = []

    @property
    def messages(self) -> list[Message]:
        return self._messages

    def add_system(self, content: str):
        self._messages.append(Message(role=Role.SYSTEM, content=content))

    def add_user(self, content: str):
        self._messages.append(Message(role=Role.USER, content=content))

    def add_assistant(self, content: str):
        self._messages.append(Message(role=Role.ASSISTANT, content=content))

    def add_message(self, message: Message):
        self._messages.append(message)

    def remove_message(self, index: int):
        del self._messages[index]

    # Basically merging array - array_merge() in php
    def add_messages(self, messages: list[Message]):
        self._messages.extend(messages)
