import os
import pandas as pd
from typing import List, Dict, Any, Tuple
from pypdf import PdfReader
import docx


class DocumentLoader:
    """Extracts raw text and metadata from uploaded files (PDF, DOCX, TXT, CSV)."""

    @staticmethod
    def load_file(file_path: str, filename: str) -> Tuple[List[Dict[str, Any]], str]:
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            return DocumentLoader._load_pdf(file_path), "pdf"
        elif ext == ".docx":
            return DocumentLoader._load_docx(file_path), "docx"
        elif ext in [".txt", ".md"]:
            return DocumentLoader._load_txt(file_path), "txt"
        elif ext == ".csv":
            return DocumentLoader._load_csv(file_path), "csv"
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _load_pdf(file_path: str) -> List[Dict[str, Any]]:
        reader = PdfReader(file_path)
        pages = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({
                    "content": text.strip(),
                    "page_number": idx + 1
                })
        return pages

    @staticmethod
    def _load_docx(file_path: str) -> List[Dict[str, Any]]:
        doc = docx.Document(file_path)
        full_text = []
        for p in doc.paragraphs:
            if p.text.strip():
                full_text.append(p.text.strip())

        text_block = "\n".join(full_text)
        return [{"content": text_block, "page_number": 1}] if text_block else []

    @staticmethod
    def _load_txt(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()
        return [{"content": text, "page_number": 1}] if text else []

    @staticmethod
    def _load_csv(file_path: str) -> List[Dict[str, Any]]:
        df = pd.read_csv(file_path)
        summary = f"CSV File with columns: {list(df.columns)}\nTotal rows: {len(df)}\n"
        sample_str = df.head(50).to_string(index=False)
        full_content = summary + "\nSample Data:\n" + sample_str
        return [{"content": full_content, "page_number": 1}]
