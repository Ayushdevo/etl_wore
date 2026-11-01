import sqlite3

from etl_wore.loaders.sqlite_loader import SqliteLoader


def test_absent_null_and_empty_values_remain_distinguishable(tmp_path):
    path = tmp_path / "rows.db"
    sink = SqliteLoader(path, "rows")
    sink.load(
        [
            {"id": 1, "value": "present"},
            {"id": 2},
            {"id": 3, "value": ""},
            {"id": 4, "value": None},
        ]
    )
    sink.close()
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT value FROM rows ORDER BY id").fetchall() == [
            ("present",),
            (None,),
            ("",),
            (None,),
        ]
