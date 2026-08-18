from app.embeddings.ollama import OllamaEmbedding
from app.models.document import Document
from app.rag.chunker import DocumentChunker
from app.rag.indexer import KnowledgeIndexer
from app.rag.retriever import Retriever
from app.vector_store.memory import MemoryVectorStore

embedding = OllamaEmbedding()
vector_store = MemoryVectorStore()
chunker = DocumentChunker()

indexer = KnowledgeIndexer(
    chunker=chunker, embedding=embedding, vector_store=vector_store
)

retreiver = Retriever(embedding=embedding, vector_store=vector_store)

document = Document(
    id="faq-001",
    title="Password Reset",
    content="""
    To reset your password, open the account settings page.
    Go the the security and select reset password.
    Enter your current password and your new password.

    Youv can also contact customer supoport if you cannot access
    your account.
    """,
)

indexer.index(document=document)

results = retreiver.retrieve(query="How can I change my password?", limit=3)

for result in results:
    print(result.content)
    print("---")
