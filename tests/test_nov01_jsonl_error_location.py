import pytest

from etl_wore.exceptions import ExtractionError
from etl_wore.extractors.json_extractor import JsonExtractor


def test_malformed_jsonl_identifies_the_actual_line(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text('\n{"id":1}\n{broken}\n')
    records = JsonExtractor(path, is_lines=True).extract()
    assert next(records) == {"id": 1}
    with pytest.raises(ExtractionError, match="line 3"):
        next(records)
