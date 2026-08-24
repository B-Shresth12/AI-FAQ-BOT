from app.models.conversation import Conversation
from app.models.document_chunk import DocumentChunk
from app.rag.context_builder import RAGContextBuilder

conversation = Conversation()

conversation.add_system("You are a helpful FAQ assistant.")


conversation.add_user("How do I reset my password?")

chunks = [
    DocumentChunk(
        id="faq-001-1",
        document_id="faq-001",
        content="To reset your password, open the account settings page.",
    ),
    DocumentChunk(
        id="faq-001-2",
        document_id="faq-001",
        content="Go to the security section and select reset password.",
    ),
]

builder = RAGContextBuilder()

context = builder.build(conversation=conversation, chunks=chunks)

for message in context.messages:
    print(message.role.value, ":", message.content)
