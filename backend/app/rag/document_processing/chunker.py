"""
Text splitting and chunking strategies.
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len,
        )

    def chunk_text(self, text: str) -> list[str]:
        """Split text into manageable chunks."""
        if not text:
            return []
        return self.splitter.split_text(text)

chunker = DocumentChunker()
