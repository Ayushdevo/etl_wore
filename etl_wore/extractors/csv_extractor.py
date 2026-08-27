"""
CSV file extractor with delimiter sniffing.
"""
import csv
import os
from typing import Generator, Dict, Any
from .base import BaseExtractor
from ..exceptions import ExtractionError

class CsvExtractor(BaseExtractor):
    def __init__(self, filepath: str, delimiter: str = None, encoding: str = "utf-8"):
        super().__init__(name=f"CsvExtractor({os.path.basename(filepath)})")
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding

    def extract(self) -> Generator[Dict[str, Any], None, None]:
        if not os.path.isfile(self.filepath):
            raise ExtractionError(f"CSV file not found: {self.filepath}")

        try:
            with open(self.filepath, mode="r", encoding=self.encoding) as f:
                if not self.delimiter:
                    sample = f.read(2048)
                    f.seek(0)
                    dialect = csv.Sniffer().sniff(sample)
                    delimiter = dialect.delimiter
                else:
                    delimiter = self.delimiter

                reader = csv.DictReader(f, delimiter=delimiter)
                for row_idx, row in enumerate(reader):
                    yield dict(row)
        except Exception as e:
            raise ExtractionError(f"Error reading CSV {self.filepath}: {e}") from e
