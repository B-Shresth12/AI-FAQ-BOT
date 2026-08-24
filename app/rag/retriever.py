from app.embeddings.base import Embedding
from app.models.document_chunk import DocumentChunk
from app.vector_store.memory import MemoryVectorStore


class Retriever:
    def __init__(self, embedding: Embedding, vector_store: MemoryVectorStore):
        self.embedding = embedding
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[DocumentChunk]:
        query_embedding = self.embedding.embed(query)

        return self.vector_store.search(embedding=query_embedding, limit=limit)
