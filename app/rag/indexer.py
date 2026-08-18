from app.embeddings.base import Embedding
from app.models.document import Document
from app.rag.chunker import DocumentChunk
from app.vector_store.base import VectorStore


class KnowledgeIndexer:
    def __init__(
        self, chunker: DocumentChunk, embedding: Embedding, vector_store: VectorStore
    ):
        self.chunker = chunker
        self.embedding = embedding
        self.vector_store = vector_store

    def index(self, document: Document) -> None:
        chunks = self.chunker.chunk(document)

        for chunk in chunks:
            embedding = self.embedding.embed(chunk.content)

            self.vector_store.add(chunk=chunk, embedding=embedding)
