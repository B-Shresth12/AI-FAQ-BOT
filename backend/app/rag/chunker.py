from app.config.settings import settings
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class DocumentChunker:
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def chunk(self, document: Document) -> list[DocumentChunk]:
        chunks = []

        start = 0
        content = document.content

        while start < len(content):
            end = start + self.chunk_size

            chunk_content = content[start:end]

            chunks.append(
                DocumentChunk(
                    id=f"{document.id}-{len(chunks) + 1}",
                    document_id=document.id,
                    content=chunk_content,
                )
            )

            if end >= len(content):
                break

            start = end - self.chunk_overlap

        return chunks
