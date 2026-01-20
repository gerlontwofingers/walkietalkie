from text_review_01.utils.base_classes import BaseDocumentReader

class TextFileReader(BaseDocumentReader):
    def supports_format(self, source: str) -> bool:
        return not source.startswith(('http://', 'https://')) and (
            source.lower().endswith('.txt') or 
            '/' not in source  # Assume it's a local file without extension
        )
    
    def load(self, source: str) -> tuple[bool, str]:
        # Your existing file loading logic here
        try:
            with open(source, 'r', encoding='utf-8') as file:
                return True, file.read()
        except UnicodeDecodeError:
            with open(source, 'r', encoding='latin-1') as file:
                return True, file.read()
        except Exception as e:
            return False, f"Error loading text file: {e}"

class URLTextReader(BaseDocumentReader):
    def supports_format(self, source: str) -> bool:
        return source.startswith(('http://', 'https://'))
    
    def load(self, source: str) -> tuple[bool, str]:
        # Your existing URL loading logic here
        try:
            import requests
            response = requests.get(source, timeout=30)
            response.raise_for_status()
            return True, response.text
        except Exception as e:
            return False, f"Error loading URL: {e}"

# Future readers (easy to add later)
class PDFReader(BaseDocumentReader):
    def supports_format(self, source: str) -> bool:
        return source.lower().endswith('.pdf')
    
    def load(self, source: str) -> tuple[bool, str]:
        # To be implemented later with PyMuPDF or similar
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(source)
            text = ""
            for page in doc:
                text += page.get_text()
            return True, text
        except Exception as e:
            return False, f"Error loading PDF: {e}"
