from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder
from app.chat.token_counter import TokenCounter

builder = ConversationBuilder()
conversation = builder.build()

conversation.add_user("My name is Bishal Shrestha.")
conversation.add_assistant("Nice to meet you, Bishal.")
conversation.add_user("what is my name?")
conversation.add_assistant("Your name is Bishal Shrestha.")
conversation.add_user("TESTING this comment")

context_manager = ContextManager()
counter = TokenCounter()

print("Before:", counter.count(conversation))

context_manager.trim(conversation)

print("After:", counter.count(conversation))

for message in conversation.messages:
    print(message.role.value, ":", message.content)
