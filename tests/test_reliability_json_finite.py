import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.exceptions import ExtractionError
class TestFinite(unittest.TestCase):
    def test_nonfinite(self):
        for literal in ['NaN','Infinity','-Infinity']:
            for lines in [False,True]:
                with self.subTest(literal=literal,lines=lines), tempfile.TemporaryDirectory() as root:
                    path=Path(root)/'in.json'; path.write_text('{"value":'+literal+'}')
                    with self.assertRaises(ExtractionError): list(JsonExtractor(str(path),is_lines=lines).extract())
