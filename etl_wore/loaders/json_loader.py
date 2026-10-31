"""
JSON Lines (JSONL) destination loader.
"""
import json
import os
from typing import List, Dict, Any
from .base import BaseLoader
from ..exceptions import LoadingError

def _validate_keys(value, active=None):
    if not isinstance(value, (dict, list, tuple)):
        return
    active = set() if active is None else active
    if id(value) in active:
        raise ValueError('Circular JSON container')
    active.add(id(value))
    try:
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise ValueError('JSON object keys must be strings')
            children = value.values()
        else:
            children = value
        for child in children:
            _validate_keys(child, active)
    finally:
        active.remove(id(value))


class JsonLinesLoader(BaseLoader):
    def __init__(self, output_path: str):
        super().__init__(name=f"JsonLinesLoader({os.path.basename(output_path)})")
        self.output_path = output_path

    def load(self, records: List[Dict[str, Any]]):
        if not records:
            return

        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
            if any(not isinstance(record, dict) for record in records):
                raise ValueError("JSONL records must be objects")
            for record in records:
                _validate_keys(record)
            lines = [json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n" for record in records]
            # Check the complete batch before opening the destination for append.
            for line in lines:
                line.encode('utf-8')
            needs_separator = False
            if os.path.exists(self.output_path) and os.path.getsize(self.output_path):
                with open(self.output_path, "rb") as existing:
                    existing.seek(-1, os.SEEK_END)
                    needs_separator = existing.read(1) not in (b"\n", b"\r")
            with open(self.output_path, "a", encoding="utf-8") as f:
                if needs_separator:
                    f.write("\n")
                f.writelines(lines)
        except Exception as e:
            raise LoadingError(f"Failed to write JSONL records to {self.output_path}: {e}") from e

