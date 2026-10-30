import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.exceptions import ExtractionError
class TestArray(unittest.TestCase):
    def test_no_partial_array(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'in.json'; path.write_text('[{"id":1}, null]')
            records=JsonExtractor(str(path)).extract()
            with self.assertRaisesRegex(ExtractionError, 'index 1'): next(records)
