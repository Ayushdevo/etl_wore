import pytest
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.exceptions import LoadingError
@pytest.mark.parametrize('records', [[None], [{'id': 1}, None], [{}], [{1: 'bad'}]])
def test_invalid_rows_raise_loading_error_without_creating_database(tmp_path, records):
    path = tmp_path / 'out.db'
    with pytest.raises(LoadingError):
        SqliteLoader(str(path), 'rows').load(records)
    assert not path.exists()
