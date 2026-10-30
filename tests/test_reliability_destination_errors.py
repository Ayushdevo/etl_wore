import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.loaders.json_loader import JsonLinesLoader
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.exceptions import LoadingError
class TestErrors(unittest.TestCase):
    def test_setup_errors(self):
        for loader in [CsvLoader('blocked/out.csv'),JsonLinesLoader('blocked/out.jsonl'),SqliteLoader('blocked/out.db','rows')]:
            with self.subTest(loader=loader.name), patch('os.makedirs',side_effect=PermissionError('denied')):
                with self.assertRaises(LoadingError): loader.load([{'id':1}])
    def test_connect_error(self):
        with tempfile.TemporaryDirectory() as root:
            loader=SqliteLoader(root,'rows')
            with self.assertRaises(LoadingError): loader.load([{'id':1}])
