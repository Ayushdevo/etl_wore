import pytest
from etl_wore.utils.retry import retry

@pytest.mark.parametrize('exceptions', ['ValueError', [ValueError], (ValueError, 'TypeError'), (str,), 123])
def test_malformed_retry_filters_fail_at_configuration_time(exceptions):
    with pytest.raises(ValueError, match='exceptions'):
        retry(exceptions=exceptions)

def test_valid_exception_class_and_tuple_still_retry():
    for filter_ in (ValueError, (ValueError, TypeError)):
        calls = []
        @retry(exceptions=filter_, initial_delay=0)
        def function():
            calls.append(1)
            if len(calls) < 2: raise ValueError('temporary')
            return 42
        assert function() == 42
        assert len(calls) == 2
