
from text_review_01.utils.chunker import DocumentChunker
from text_review_01.utils.readers import TextFileReader, URLTextReader


class DocumentProcessor:
    def __init__(self):
        self.readers = [
            TextFileReader(),
            URLTextReader(),
            # PDFReader(),  # Add when ready
            # EpubReader(), # Add when ready  
        ]
        self.chunker = DocumentChunker()
    
    def process_document(self, source: str, chunk_size=800, chunk_overlap=100) -> dict:
        """Main entry point - finds appropriate reader and processes document"""
        
        # Find a reader that supports this format
        reader = None
        for r in self.readers:
            if r.supports_format(source):
                reader = r
                break
        
        if not reader:
            return {
                "success": False,
                "error": f"No reader found for source: {source}",
                "chunks": []
            }
        
        # Load the document
        success, content = reader.load(source)
        if not success:
            return {
                "success": False,
                "error": content,  # error message is returned in content
                "chunks": []
            }
        
        # Chunk the content
        self.chunker.chunk_size = chunk_size
        self.chunker.chunk_overlap = chunk_overlap
        chunks = self.chunker.chunk_text(content)
        
        return {
            "success": True,
            "source": source,
            "reader_type": type(reader).__name__,
            "total_chars": len(content),
            "total_tokens": self.chunker.count_tokens(content),
            "chunks": chunks,
            "chunk_count": len(chunks)
        }
