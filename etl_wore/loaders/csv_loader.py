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
            has_content = os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0
            if has_content:
                with open(self.output_path, newline="", encoding="utf-8") as existing:
                    headers = next(csv.reader(existing, delimiter=self.delimiter))
            # Validate the whole batch before appending any rows.
            if any(set(record) - set(headers) for record in records):
                raise ValueError("Record contains columns absent from the CSV header")
            mode = "a" if has_content else "w"
            write_header = not has_content

            with open(self.output_path, mode=mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers, delimiter=self.delimiter)
                if write_header:
                    writer.writeheader()
                writer.writerows(records)

            self._initialized = True
        except Exception as e:
            raise LoadingError(f"Failed to write CSV records to {self.output_path}: {e}") from e
