import pytest
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.exceptions import LoadingError
@pytest.mark.parametrize('name', [None, 12, '', 'a\x00b'])
def test_bad_table_name_fails_at_construction(name):
    with pytest.raises(ValueError):
        SqliteLoader(':memory:', name)
def test_case_colliding_columns_fail_before_schema_creation(tmp_path):
    loader = SqliteLoader(str(tmp_path / 'out.db'), 'rows')
    with pytest.raises(LoadingError, match='unique'):
        loader.load([{'ID': 1, 'id': 2}])
    assert loader._conn is None
