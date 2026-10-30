import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.exceptions import ExtractionError
class TestRagged(unittest.TestCase):
    def test_ragged(self):
        for data in ['id,name\n1,Alice,extra\n', 'id,name\n1\n']:
            with self.subTest(data=data), tempfile.TemporaryDirectory() as root:
                path=Path(root)/'in.csv'; path.write_text(data)
                with self.assertRaisesRegex(ExtractionError, 'line 2'): list(CsvExtractor(str(path), delimiter=',').extract())
