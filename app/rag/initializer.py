from app.rag.indexer import KnowledgeIndexer
from app.rag.knowledge_loader import KnowlegeLoader


class KnowledgeInitializer:
    def __init__(self, loader: KnowlegeLoader, indexer: KnowledgeIndexer):
        self.loader = loader
        self.indexer = indexer

    def initialize(self) -> None:
        documents = self.loader.load()

        for document in documents:
            self.indexer.index(document=document)
