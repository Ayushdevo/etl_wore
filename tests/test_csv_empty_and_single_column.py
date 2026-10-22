import pytest
from etl_wore.extractors.csv_extractor import CsvExtractor

@pytest.mark.parametrize("text, expected", [("", []), ("id\n1\n2\n", [{"id": "1"}, {"id": "2"}]), ('id,name\n1,"hello\r\nworld"\n', [{"id": "1", "name": "hello\r\nworld"}])])
def test_csv_shapes(tmp_path, text, expected):
    path = tmp_path / "data.csv"
    path.write_bytes(text.encode())
    assert list(CsvExtractor(str(path)).extract()) == expected
