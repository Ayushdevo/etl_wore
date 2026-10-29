import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.transformers.schema_validator import SchemaValidator
from etl_wore.exceptions import TransformationError
class TestOverflow(unittest.TestCase):
    def test_overflow(self):
        with self.assertRaises(TransformationError): SchemaValidator({'id':int}).transform({'id':float('inf')})
        self.assertIsNone(SchemaValidator({'id':int},drop_invalid=True).transform({'id':float('inf')}))
