from abc import ABC, abstractmethod
from typing import Optional

class BaseDocumentReader(ABC):
    @abstractmethod
    def load(self, source: str) -> tuple[bool, str]:
        """Load document and return (success, text_content)"""
        pass
    
    @abstractmethod
    def supports_format(self, source: str) -> bool:
        """Check if this reader can handle the given source"""
        pass
