class DocumentChunk:
    def __init__(
        self,
        id: str,
        document_id: str,
        content: str,
    ):
        self.id = id
        self.document_id = document_id
        self.content = content
