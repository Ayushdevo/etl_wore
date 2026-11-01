"""
Data Sanitizer for string cleanup and sensitive data masking.
"""
from typing import Dict, Any, Optional, List
from .base import BaseTransformer

class DataSanitizer(BaseTransformer):
    def __init__(self, strip_strings: bool = True, mask_fields: Optional[List[str]] = None):
        super().__init__()
        if not isinstance(strip_strings, bool):
            raise ValueError("strip_strings must be a boolean")
        if mask_fields is not None and (not isinstance(mask_fields, (list, tuple)) or any(not isinstance(field, str) or not field for field in mask_fields)):
            raise ValueError("mask_fields must be a sequence of nonempty field names")
        self.strip_strings = strip_strings
        self.mask_fields = set(mask_fields or [])

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        out = {}
        for k, v in record.items():
            if isinstance(v, str) and self.strip_strings:
                v = v.strip()
            if k in self.mask_fields:
                v = "***MASKED***"
            out[k] = v
        return out
