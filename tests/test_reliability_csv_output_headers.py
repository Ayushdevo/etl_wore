import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.exceptions import LoadingError
class TestOutputHeaders(unittest.TestCase):
    def test_bad_schema(self):
        for record in [{}, {'':1}, {1:'integer','1':'string'}]:
            with self.subTest(record=record), tempfile.TemporaryDirectory() as root:
                path=Path(root)/'out.csv'
                with self.assertRaises(LoadingError): CsvLoader(str(path)).load([record])
                self.assertFalse(path.exists())
    def test_bad_existing_header(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'out.csv'; path.write_text('id,id\n1,2\n')
            before=path.read_bytes()
            with self.assertRaises(LoadingError): CsvLoader(str(path)).load([{'id':3}])
            self.assertEqual(path.read_bytes(), before)
