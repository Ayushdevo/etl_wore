import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.transformers.schema_validator import SchemaValidator
class TestNumericBool(unittest.TestCase):
    def test_numeric_type(self):
        out=SchemaValidator({'count':int}).transform({'count':True})
        self.assertIs(type(out['count']),int)
        self.assertEqual(out['count'],1)
