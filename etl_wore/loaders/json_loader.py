"""
JSON Lines (JSONL) destination loader.
"""
import json
import os
from typing import List, Dict, Any
from .base import BaseLoader
from ..exceptions import LoadingError

class JsonLinesLoader(BaseLoader):
    def __init__(self, output_path: str):
        super().__init__(name=f"JsonLinesLoader({os.path.basename(output_path)})")
        self.output_path = output_path

    def load(self, records: List[Dict[str, Any]]):
        if not records:
            return

        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                for record in records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            raise LoadingError(f"Failed to write JSONL records to {self.output_path}: {e}") from e
