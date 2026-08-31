"""
Abstract Base Transformer.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseTransformer(ABC):
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform or filter a single record. Return None to drop."""
        pass
