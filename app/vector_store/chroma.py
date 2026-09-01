import chromadb

from app.config.settings import settings
from app.models.document_chunk import DocumentChunk
from app.vector_store.base import VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

    def add(
        self,
        chunk: DocumentChunk,
        embedding: list[float],
    ) -> None:
        self.collection.upsert(
            ids=[chunk.id],
            embeddings=[embedding],
            documents=[chunk.content],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                }
            ],
        )

    def search(self, embedding: list[float], limit: int = 5) -> list[DocumentChunk]:
        results = self.collection.query(query_embeddings=[embedding], n_results=limit)

        chunks = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for id, content, metadata in zip(ids, documents, metadatas):
            chunks.append(
                DocumentChunk(
                    id=id,
                    document_id=metadata["docuemnt_id"],
                    content=content,
                )
            )

        return chunks
