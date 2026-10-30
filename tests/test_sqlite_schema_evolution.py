import sqlite3
import pytest
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.exceptions import LoadingError


def test_new_batch_columns_extend_existing_table_without_losing_rows(tmp_path):
    path = tmp_path / "records.db"
    loader = SqliteLoader(str(path), 'order "details"')
    loader.load([{"id": 1}])
    loader.load([{"id": 2, 'new "field"': "value"}])
    loader.close()
    with sqlite3.connect(path) as conn:
        assert conn.execute('SELECT * FROM "order ""details""" ORDER BY id').fetchall() == [("1", None), ("2", "value")]


def test_failed_batch_rolls_back_column_additions(tmp_path):
    path = tmp_path / "records.db"
    loader = SqliteLoader(str(path), "records")
    loader.load([{"id": 1}])
    class Unserializable:
        def __str__(self):
            raise ValueError("cannot serialize")
    with pytest.raises(LoadingError):
        loader.load([{"id": 2, "new": Unserializable()}])
    loader.close()
    with sqlite3.connect(path) as conn:
        assert [row[1] for row in conn.execute('PRAGMA table_info("records")')] == ["id"]
        assert conn.execute("SELECT * FROM records").fetchall() == [("1",)]
