"""
Unit tests for data loaders.
"""
import tempfile
import os
import sqlite3
from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.loaders.sqlite_loader import SqliteLoader

def test_csv_loader():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
        path = tmp.name

    try:
        loader = CsvLoader(path)
        loader.load([{"a": "1", "b": "2"}, {"a": "3", "b": "4"}])
        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 3
    finally:
        os.remove(path)

def test_sqlite_loader():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        loader = SqliteLoader(db_path, "test_table")
        loader.load([{"col1": "val1", "col2": "val2"}])
        loader.close()

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT col1, col2 FROM test_table")
        rows = cur.fetchall()
        assert rows == [("val1", "val2")]
        conn.close()
    finally:
        os.remove(db_path)
