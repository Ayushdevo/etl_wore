import csv
import pytest
from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.exceptions import LoadingError

def test_existing_empty_file_gets_header(tmp_path):
    path = tmp_path / "out.csv"
    path.touch()
    CsvLoader(str(path)).load([{"a": "1", "b": "2"}])
    assert list(csv.DictReader(path.open())) == [{"a": "1", "b": "2"}]

def test_append_respects_existing_header(tmp_path):
    path = tmp_path / "out.csv"
    loader = CsvLoader(str(path))
    loader.load([{"a": "1", "b": "2"}])
    loader.load([{"b": "4", "a": "3"}])
    CsvLoader(str(path)).load([{"b": "6", "a": "5"}])
    assert list(csv.DictReader(path.open())) == [{"a":"1","b":"2"},{"a":"3","b":"4"},{"a":"5","b":"6"}]
    before = path.read_bytes()
    with pytest.raises(LoadingError):
        loader.load([{"a":"7","b":"8"},{"a":"9","b":"10","extra":"bad"}])
    assert path.read_bytes() == before
