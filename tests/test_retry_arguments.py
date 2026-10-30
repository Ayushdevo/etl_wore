import pytest
from etl_wore.utils.retry import retry

@pytest.mark.parametrize("kwargs", [{"max_attempts": 0}, {"max_attempts": -1}, {"max_attempts": 1.5}, {"max_attempts": True}, {"initial_delay": -1}, {"initial_delay": float("nan")}, {"backoff_factor": 0}, {"backoff_factor": float("inf")}])
def test_invalid_retry_configuration(kwargs):
    with pytest.raises(ValueError):
        retry(**kwargs)
