"""
Deduplication transformer using key hashes.
"""
from typing import Dict, Any, Optional, List
from .base import BaseTransformer

class DeduplicationTransformer(BaseTransformer):
    def __init__(self, key_fields: List[str]):
        super().__init__()
        self.key_fields = key_fields
        self._seen_keys = set()

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        composite_key = tuple(record.get(k) for k in self.key_fields)
        if composite_key in self._seen_keys:
            return None  # Drop duplicate
        self._seen_keys.add(composite_key)
        return record
