import pytest

from etl_wore.utils.retry import retry


@pytest.mark.parametrize("name", ["initial_delay", "backoff_factor"])
@pytest.mark.parametrize("value", [True, "1", None, 10**1000])
def test_bad_delay_configuration_is_a_value_error(name, value):
    with pytest.raises(ValueError):
        retry(**{name: value})
