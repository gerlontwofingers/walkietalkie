
import tiktoken


class DocumentChunker:
    def __init__(self, chunk_size=800, chunk_overlap=100, model_name="gpt-3.5-turbo"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.encoding_for_model(model_name)
    
    def chunk_text(self, text: str) -> list[str]:
        """Pure chunking logic - no file handling concerns"""
        if not text.strip():
            return []
        
        # Your existing smart_chunking logic here
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for paragraph in paragraphs:
            para_tokens = self.count_tokens(paragraph)
            
            if para_tokens > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                    current_tokens = 0
                
                large_chunks = self._split_large_paragraph(paragraph)
                for small_chunk in large_chunks:
                    # ... existing chunking logic
                    pass
            else:
                # ... existing chunking logic
                pass
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))
    
    def _split_large_paragraph(self, paragraph: str) -> list[str]:
        # ... your existing implementation
        pass
    
    def _create_token_overlap(self, text: str) -> str:
        # ... your existing implementation
        pass
