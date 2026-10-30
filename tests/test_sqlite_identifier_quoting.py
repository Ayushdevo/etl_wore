import sqlite3
from etl_wore.loaders.sqlite_loader import SqliteLoader

def test_quoted_table_and_column_names(tmp_path):
    path = str(tmp_path / "data.db")
    loader = SqliteLoader(path, 'orders"archive')
    loader.load([{'a"b': "one", 'back`tick': "two"}])
    loader.close()
    with sqlite3.connect(path) as conn:
        assert conn.execute('SELECT * FROM "orders""archive"').fetchall() == [("one", "two")]
