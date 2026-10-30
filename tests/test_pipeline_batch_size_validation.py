import pytest
from etl_wore.pipeline.engine import Pipeline

@pytest.mark.parametrize("size", [0, -1, 1.5, True, "2"])
def test_batch_size_must_be_positive_integer(size):
    with pytest.raises(ValueError):
        Pipeline("test", batch_size=size)
