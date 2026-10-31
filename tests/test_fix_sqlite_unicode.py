import sqlite3
from etl_wore.loaders.sqlite_loader import SqliteLoader

def test_unicode_columns_remain_distinct_during_schema_evolution(tmp_path):
    path = tmp_path / 'records.db'
    loader = SqliteLoader(str(path), 'records')
    loader.load([{'Ä':'first'}])
    loader.load([{'ä':'second'}])
    loader.close()
    with sqlite3.connect(path) as connection:
        assert [r[1] for r in connection.execute('PRAGMA table_info(records)')] == ['Ä', 'ä']
        assert connection.execute('SELECT "Ä", "ä" FROM records').fetchall() == [('first', None), (None, 'second')]
