import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from etl_wore.pipeline.context import PipelineContext
class TestDuration(unittest.TestCase):
    def test_wall_clock_jump(self):
        with patch('etl_wore.pipeline.context.time.time',side_effect=[100,50]), patch('etl_wore.pipeline.context.time.monotonic',side_effect=[10,12]):
            ctx=PipelineContext(); ctx.finish()
            self.assertEqual(ctx.duration_seconds,2)
    def test_finish_is_idempotent(self):
        with patch('etl_wore.pipeline.context.time.time',side_effect=[100,102,110]), patch('etl_wore.pipeline.context.time.monotonic',side_effect=[10,12,20]):
            ctx=PipelineContext(); ctx.finish(); first=ctx.duration_seconds; end=ctx.end_time
            ctx.finish()
            self.assertEqual(ctx.duration_seconds,first)
            self.assertEqual(ctx.end_time,end)
