"""
Date Normalizer to standard ISO 8601 formatting.
"""
from datetime import timezone
from typing import Dict, Any, Optional, List
import dateutil.parser
from .base import BaseTransformer

class DateNormalizer(BaseTransformer):
    def __init__(self, date_fields: List[str], output_format: str = "%Y-%m-%dT%H:%M:%SZ"):
        super().__init__()
        if not isinstance(date_fields, (list, tuple)) or not date_fields or any(not isinstance(field, str) or not field for field in date_fields):
            raise ValueError("date_fields must be a nonempty sequence of field names")
        if not isinstance(output_format, str) or not output_format:
            raise ValueError("output_format must be a nonempty string")
        self.date_fields = tuple(date_fields)
        self.output_format = output_format

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        out = dict(record)
        for field in self.date_fields:
            raw_val = out.get(field)
            if raw_val:
                try:
                    parsed = dateutil.parser.parse(str(raw_val))
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    parsed = parsed.astimezone(timezone.utc)
                    out[field] = parsed.strftime(self.output_format)
                except Exception:
                    pass
        return out
