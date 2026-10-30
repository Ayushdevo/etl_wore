import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys
from etl_wore.cli import main
class TestNoop(unittest.TestCase):
    def test_no_false_success(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'spec.json'; path.write_text('{"name":"demo"}')
            with patch.object(sys,'argv',['etl-wore','--spec',str(path)]):
                with self.assertRaises(SystemExit) as exc: main()
            self.assertNotEqual(exc.exception.code,0)
