import sqlite3
from etl_wore.loaders.sqlite_loader import SqliteLoader

def test_none_remains_sql_null(tmp_path):
    path = str(tmp_path / "data.db")
    loader = SqliteLoader(path, "records")
    loader.load([{"value": None}, {"value": "None"}])
    loader.close()
    with sqlite3.connect(path) as conn:
        assert conn.execute("SELECT value FROM records").fetchall() == [(None,), ("None",)]
