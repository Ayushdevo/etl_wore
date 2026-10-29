import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.exceptions import ExtractionError
class TestQuotes(unittest.TestCase):
    def test_unterminated(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'in.csv'; path.write_text('id,name\n1,"unfinished\n')
            with self.assertRaises(ExtractionError): list(CsvExtractor(str(path), delimiter=',').extract())
    def test_quoted_newline(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'in.csv'; path.write_text('id,name\n1,"Alice\nBob"\n')
            self.assertEqual(list(CsvExtractor(str(path), delimiter=',').extract())[0]['name'], 'Alice\nBob')
