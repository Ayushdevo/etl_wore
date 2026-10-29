import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import json
from etl_wore.loaders.json_loader import JsonLinesLoader
class TestBoundary(unittest.TestCase):
    def test_boundary(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'out.jsonl'; path.write_text('{"id": 1}')
            JsonLinesLoader(str(path)).load([{'id':2}])
            self.assertEqual([json.loads(line) for line in path.read_text().splitlines()], [{'id':1},{'id':2}])
