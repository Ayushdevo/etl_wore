"""
Abstract Base Loader.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLoader(ABC):
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def load(self, records: List[Dict[str, Any]]):
        """Persist a batch of records to destination."""
        pass

    def close(self):
        """Flush or close open connection resources."""
        pass
