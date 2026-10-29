import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import threading
from etl_wore.pipeline.parallel import ParallelBatchLoader
class TestSnapshot(unittest.TestCase):
    def test_nested_snapshot(self):
        release=threading.Event(); observed=[]
        base=Mock(); base.name='test'
        def load(records):
            if not release.wait(2): raise RuntimeError('test synchronization timed out')
            observed.extend(records)
        base.load.side_effect=load
        loader=ParallelBatchLoader(base,max_workers=1)
        record={'nested':{'tags':['original']}}
        try:
            loader.load([record])
            record['nested']['tags'].append('mutated')
        finally:
            release.set(); loader.close()
        self.assertEqual(observed,[{'nested':{'tags':['original']}}])
