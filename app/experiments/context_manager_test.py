from app.chat.context_manager import ContextManager
from app.chat.conversation_builder import ConversationBuilder

builder = ConversationBuilder()
conversation = builder.build()

conversation.add_user("My name is Bishal Shrestha.")
conversation.add_assistant("Nice to meet you, Bishal.")
conversation.add_user("what is my name?")

context_manager = ContextManager()

print("Fits: ", context_manager.fits(conversation=conversation))
