import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import logging
from etl_wore.cli import main, logger
class TestVerbose(unittest.TestCase):
    def test_verbose(self):
        previous=logger.level
        try:
            with tempfile.TemporaryDirectory() as root:
                path=Path(root)/'spec.json'; path.write_text('{}')
                with patch.object(sys,'argv',['etl-wore','--spec',str(path),'--dry-run','--verbose']):
                    with self.assertRaises(SystemExit): main()
                self.assertEqual(logger.level,logging.DEBUG)
        finally: logger.setLevel(previous)
