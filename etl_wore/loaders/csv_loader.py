"""
CSV destination loader.
"""
import csv
import os
from typing import List, Dict, Any
from .base import BaseLoader
from ..exceptions import LoadingError

class CsvLoader(BaseLoader):
    def __init__(self, output_path: str, delimiter: str = ","):
        super().__init__(name=f"CsvLoader({os.path.basename(output_path)})")
        self.output_path = output_path
        self.delimiter = delimiter
        self._initialized = False

    def load(self, records: List[Dict[str, Any]]):
        if not records:
            return

        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        headers = list(records[0].keys())

        try:
            mode = "a" if self._initialized or os.path.exists(self.output_path) else "w"
            write_header = mode == "w"

            with open(self.output_path, mode=mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers, delimiter=self.delimiter)
                if write_header:
                    writer.writeheader()
                writer.writerows(records)

            self._initialized = True
        except Exception as e:
            raise LoadingError(f"Failed to write CSV records to {self.output_path}: {e}") from e
