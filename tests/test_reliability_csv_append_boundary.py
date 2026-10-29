import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import csv
from etl_wore.loaders.csv_loader import CsvLoader
class TestBoundary(unittest.TestCase):
    def test_boundary(self):
        for initial in ['id,name', 'id,name\n1,Alice']:
            with self.subTest(initial=initial), tempfile.TemporaryDirectory() as root:
                path=Path(root)/'out.csv'; path.write_text(initial)
                CsvLoader(str(path)).load([{'id': '2', 'name': 'Bob'}])
                with path.open(newline='') as stream: rows=list(csv.DictReader(stream))
                self.assertEqual(rows[-1], {'id':'2','name':'Bob'})
                self.assertEqual(len(rows), 1 if initial=='id,name' else 2)
