from app.embeddings.base import Embedding
from app.models.document import Document
from app.rag.chunker import DocumentChunker
from app.vector_store.base import VectorStore


class KnowledgeIndexer:
    def __init__(
        self,
        chunker: DocumentChunker,
        embedding: Embedding,
        vector_store: VectorStore,
    ):
        self.chunker = chunker
        self.embedding = embedding
        self.vector_store = vector_store

    def index(self, document: Document) -> None:
        print("Indexing:", document.title)

        chunks = self.chunker.chunk(document)

        print("Chunks:", len(chunks))

        for chunk in chunks:
            print("Embedding chunk:", chunk.id)

            embedding = self.embedding.embed(chunk.content)

            print("Embedding size:", len(embedding))

            self.vector_store.add(
                chunk=chunk,
                embedding=embedding,
            )

        print("Indexing complete")
