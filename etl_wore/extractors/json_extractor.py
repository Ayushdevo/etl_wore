"""
JSON and JSON Lines extractor.
"""
import json
import os
from typing import Generator, Dict, Any
from .base import BaseExtractor
from ..exceptions import ExtractionError

class JsonExtractor(BaseExtractor):
    def __init__(self, filepath: str, is_lines: bool = False, encoding: str = "utf-8"):
        super().__init__(name=f"JsonExtractor({os.path.basename(filepath)})")
        self.filepath = filepath
        self.is_lines = is_lines
        self.encoding = encoding

    def extract(self) -> Generator[Dict[str, Any], None, None]:
        if not os.path.isfile(self.filepath):
            raise ExtractionError(f"JSON file not found: {self.filepath}")

        try:
            with open(self.filepath, "r", encoding=self.encoding) as f:
                if self.is_lines:
                    for line_no, line in enumerate(f, start=1):
                        line = line.strip()
                        if line:
                            yield json.loads(line)
                else:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            yield item
                    elif isinstance(data, dict):
                        yield data
                    else:
                        raise ExtractionError("Top-level JSON structure must be object or array")
        except Exception as e:
            raise ExtractionError(f"Failed to extract JSON from {self.filepath}: {e}") from e
