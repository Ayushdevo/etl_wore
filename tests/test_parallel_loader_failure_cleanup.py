from unittest.mock import Mock
import pytest
from etl_wore.pipeline.parallel import ParallelBatchLoader

def test_worker_failure_still_closes_resources():
    base = Mock(name="base")
    base.load.side_effect = ValueError("worker failed")
    loader = ParallelBatchLoader(base, max_workers=1)
    loader.load([{"id":1}])
    with pytest.raises(ValueError, match="worker failed"):
        loader.close()
    base.close.assert_called_once()
    with pytest.raises(RuntimeError):
        loader.executor.submit(lambda: None)
    loader.close()  # repeated cleanup is harmless
    base.close.assert_called_once()
