"""
Date Normalizer to standard ISO 8601 formatting.
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
import dateutil.parser
from .base import BaseTransformer

class DateNormalizer(BaseTransformer):
    def __init__(self, date_fields: List[str], output_format: str = "%Y-%m-%dT%H:%M:%SZ"):
        super().__init__()
        self.date_fields = date_fields
        self.output_format = output_format

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        out = dict(record)
        for field in self.date_fields:
            raw_val = out.get(field)
            if raw_val:
                try:
                    parsed = dateutil.parser.parse(str(raw_val))
                    out[field] = parsed.strftime(self.output_format)
                except Exception:
                    pass
        return out
