from app.models.conversation import Conversation
from app.repositories.postgres_conversation_store import PostgresConversationStore

store = PostgresConversationStore()

conversation = Conversation()
conversation.add_user("Hello")
conversation.add_assistant("Hi! How can I help you?")

store.save(
    conversation_id="test-conversation",
    conversation=conversation,
)

print("Conversation saved.")