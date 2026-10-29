"""
CSV file extractor with delimiter sniffing.
"""
import csv
import os
from typing import Generator, Dict, Any
from .base import BaseExtractor
from ..exceptions import ExtractionError

class CsvExtractor(BaseExtractor):
    def __init__(self, filepath: str, delimiter: str = None, encoding: str = "utf-8-sig"):
        super().__init__(name=f"CsvExtractor({os.path.basename(filepath)})")
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding

    def extract(self) -> Generator[Dict[str, Any], None, None]:
        if not os.path.isfile(self.filepath):
            raise ExtractionError(f"CSV file not found: {self.filepath}")

        try:
            with open(self.filepath, mode="r", encoding=self.encoding, newline="") as f:
                if not self.delimiter:
                    sample = f.read(2048)
                    f.seek(0)
                    if not sample:
                        return
                    try:
                        delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
                    except csv.Error:
                        delimiter = ","
                else:
                    delimiter = self.delimiter

                reader = csv.DictReader(f, delimiter=delimiter)
                headers = reader.fieldnames
                if headers is not None and (any(not name for name in headers) or len(set(headers)) != len(headers)):
                    raise ExtractionError("CSV column names must be nonempty and unique")
                for row_idx, row in enumerate(reader):
                    if None in row or any(value is None for value in row.values()):
                        raise ExtractionError(f"CSV record at line {reader.line_num} does not match the header width")
                    yield dict(row)
        except Exception as e:
            raise ExtractionError(f"Error reading CSV {self.filepath}: {e}") from e

