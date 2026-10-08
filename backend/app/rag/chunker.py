from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument

from app.core.config import settings


class DocumentChunker:
    """Splits pages into character chunks with rich metadata for citations."""

    def __init__(self, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_document(
        self,
        pages: List[Dict[str, Any]],
        document_id: str,
        filename: str,
        user_id: str
    ) -> List[LCDocument]:
        """
        Chunks pages and produces LangChain LCDocument objects containing metadata.
        """
        lc_docs = []
        chunk_counter = 0

        for page_data in pages:
            content = page_data["content"]
            page_num = page_data.get("page_number", 1)

            splits = self.splitter.split_text(content)

            for split in splits:
                if not split.strip():
                    continue

                chunk_counter += 1
                metadata = {
                    "document_id": str(document_id),
                    "document_name": filename,
                    "user_id": str(user_id),
                    "page_number": page_num,
                    "chunk_id": f"{document_id}_chunk_{chunk_counter}",
                    "source_type": filename.split(".")[-1].lower()
                }

                lc_docs.append(LCDocument(page_content=split, metadata=metadata))

        return lc_docs
