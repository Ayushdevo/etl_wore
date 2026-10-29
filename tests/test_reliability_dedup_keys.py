import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.transformers.deduplicator import DeduplicationTransformer
class TestKeys(unittest.TestCase):
    def test_invalid_keys(self):
        for keys in [[], '', 'id', [''], [1]]:
            with self.subTest(keys=keys), self.assertRaises(ValueError): DeduplicationTransformer(keys)
    def test_valid_keys(self):
        transformer=DeduplicationTransformer(['id'])
        self.assertEqual(transformer.transform({'id':1}),{'id':1})
        self.assertIsNone(transformer.transform({'id':1}))
