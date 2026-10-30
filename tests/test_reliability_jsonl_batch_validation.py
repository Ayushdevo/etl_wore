import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.loaders.json_loader import JsonLinesLoader
from etl_wore.exceptions import LoadingError
class TestBatch(unittest.TestCase):
    def test_invalid_batch_preserves_file(self):
        for bad in [{'value':object()}, {'value':float('nan')}, ['not', 'a', 'record']]:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as root:
                path=Path(root)/'out.jsonl'; path.write_text('{"old":true}\n')
                before=path.read_bytes()
                with self.assertRaises(LoadingError): JsonLinesLoader(str(path)).load([{'id':1},bad])
                self.assertEqual(path.read_bytes(),before)
