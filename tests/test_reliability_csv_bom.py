import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.csv_extractor import CsvExtractor
class TestBom(unittest.TestCase):
    def test_bom(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'in.csv'
            path.write_text('\ufeffid,name\n1,Alice\n', encoding='utf-8')
            self.assertEqual(list(CsvExtractor(str(path)).extract()), [{'id':'1','name':'Alice'}])
