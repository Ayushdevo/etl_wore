import pytest

from etl_wore.exceptions import LoadingError
from etl_wore.loaders.csv_loader import CsvLoader


def test_unterminated_header_is_not_silently_extended(tmp_path):
    path = tmp_path / "output.csv"
    original = '"id,name\n'
    path.write_text(original)
    with pytest.raises(LoadingError):
        CsvLoader(path).load([{"id,name\n": "x"}])
    assert path.read_text() == original
