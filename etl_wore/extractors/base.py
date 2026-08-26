"""
Abstract Base Extractor.
"""
from abc import ABC, abstractmethod
from typing import Generator, Dict, Any

class BaseExtractor(ABC):
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def extract(self) -> Generator[Dict[str, Any], None, None]:
        """Yield extracted records one by one or in batches."""
        pass
