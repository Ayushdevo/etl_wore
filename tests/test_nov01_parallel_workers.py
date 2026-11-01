import pytest

from etl_wore.pipeline.parallel import ParallelBatchLoader


class Sink:
    name = "sink"

    def load(self, records):
        pass

    def close(self):
        pass


@pytest.mark.parametrize("workers", [True, False, 0, -1, 1.5, "2"])
def test_invalid_worker_counts_fail_cleanly(workers):
    with pytest.raises(ValueError):
        ParallelBatchLoader(Sink(), max_workers=workers)
