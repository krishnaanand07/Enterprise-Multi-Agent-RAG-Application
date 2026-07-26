"""
Text extraction logic for various document types.
"""
import os
from pathlib import Path
import PyPDF2
from loguru import logger

class DocumentExtractor:
    def extract_text(self, file_path: str) -> tuple[str, dict]:
        """
        Extract text and basic metadata from a file.
        Returns: (extracted_text, metadata_dict)
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext in [".txt", ".md", ".csv", ".json"]:
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Extraction not implemented for {ext}")

    def _extract_txt(self, file_path: str) -> tuple[str, dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text, {"num_pages": 1}

    def _extract_pdf(self, file_path: str) -> tuple[str, dict]:
        text = ""
        num_pages = 0
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            
        # If no text found, it might be a scanned PDF.
        # In a full production system, we would trigger Tesseract OCR here.
        if not text.strip():
            logger.warning(f"No text extracted from {file_path}. OCR needed.")
            text = "[Image-based PDF - OCR processing required]"
            
        return text, {"num_pages": num_pages}

extractor = DocumentExtractor()
