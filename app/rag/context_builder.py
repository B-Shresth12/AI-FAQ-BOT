from app.models.conversation import Conversation
from app.models.document_chunk import DocumentChunk


class RAGContextBuilder:
    def build(
        conversation: Conversation,
        chunks: list[DocumentChunk],
    ) -> Conversation:
        context = Conversation()

        for message in conversation.messages:
            context.add_message(message=message)

        if chunks:
            content = "\n\n".join(chunk.content for chunk in chunks)

            context.add_context_at(index=1, content=content)

        return context
