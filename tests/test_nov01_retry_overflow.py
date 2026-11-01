import threading
from unittest.mock import patch

import pytest

from etl_wore.utils.retry import retry


def test_overflowing_backoff_does_not_mask_original_error():
    @retry(max_attempts=3, initial_delay=1e308, backoff_factor=1e308)
    def operation():
        raise LookupError("original")

    delays = []

    def sleep(delay):
        assert 0 <= delay <= threading.TIMEOUT_MAX
        delays.append(delay)

    with patch("etl_wore.utils.retry.time.sleep", side_effect=sleep):
        with pytest.raises(LookupError, match="original"):
            operation()
    assert len(delays) == 2
