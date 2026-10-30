import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.exceptions import ExtractionError
class TestHeaders(unittest.TestCase):
    def test_headers(self):
        for data in ['id,id\n1,2\n', 'id,\n1,2\n']:
            with self.subTest(data=data), tempfile.TemporaryDirectory() as root:
                path=Path(root)/'in.csv'; path.write_text(data)
                with self.assertRaises(ExtractionError): list(CsvExtractor(str(path), delimiter=',').extract())
