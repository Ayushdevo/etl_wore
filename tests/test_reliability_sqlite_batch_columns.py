import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sqlite3
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.exceptions import LoadingError
class TestColumns(unittest.TestCase):
    def test_extra_key(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'data.db'; loader=SqliteLoader(str(path),'rows')
            try:
                with self.assertRaises(LoadingError): loader.load([{'id':1},{'id':2,'lost':'value'}])
                if path.exists():
                    with sqlite3.connect(path) as conn:
                        self.assertEqual(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(), [])
            finally: loader.close()
