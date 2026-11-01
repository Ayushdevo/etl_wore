"""
JSON and JSON Lines extractor.
"""
import json
import math
import os
from typing import Generator, Dict, Any
from .base import BaseExtractor
from ..exceptions import ExtractionError

def _reject_constant(value):
    raise ValueError(f"Invalid JSON numeric constant: {value}")


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f'JSON numbers must be finite: {value}')
    return number


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON object key: {key}')
        result[key] = value
    return result


class JsonExtractor(BaseExtractor):
    def __init__(self, filepath: str, is_lines: bool = False, encoding: str = "utf-8-sig"):
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
                            try:
                                item = json.loads(line, parse_constant=_reject_constant, parse_float=_finite_float, object_pairs_hook=_unique_object)
                            except ValueError as exc:
                                raise ExtractionError(f"Invalid JSON Lines record at line {line_no}: {exc}") from exc
                            if not isinstance(item, dict):
                                raise ExtractionError(f"JSON Lines record at line {line_no} must be an object")
                            yield item
                else:
                    data = json.load(f, parse_constant=_reject_constant, parse_float=_finite_float, object_pairs_hook=_unique_object)
                    if isinstance(data, list):
                        for index, item in enumerate(data):
                            if not isinstance(item, dict):
                                raise ExtractionError(f"JSON array record at index {index} must be an object")
                        yield from data
                    elif isinstance(data, dict):
                        yield data
                    else:
                        raise ExtractionError("Top-level JSON structure must be object or array")
        except Exception as e:
            raise ExtractionError(f"Failed to extract JSON from {self.filepath}: {e}") from e

