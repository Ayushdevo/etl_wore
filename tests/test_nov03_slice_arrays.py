import pytest
from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError

nan, inf = float("nan"), float("inf")


def build(**options):
    config = {
        "type": "slice_arrays",
        "fields": ["value"],
        "start": None,
        "stop": None,
        "step": 1,
    }
    config.update(options)
    return _component(config, _TRANSFORMERS, "transformer")


@pytest.mark.parametrize(
    "options,value,expected",
    [
        ({"start": 1, "stop": 4, "step": 2}, [0, 1, 2, 3, 4], [1, 3]),
        ({"step": -1}, [1, 2, 3], [3, 2, 1]),
        ({"start": -2}, [1, 2, 3], [2, 3]),
    ],
)
def test_conversion(options, value, expected):
    original = {"value": value, "other": {"nested": [1]}}
    result = build(**options).transform(original)
    assert result == {"value": expected, "other": {"nested": [1]}}
    result["other"]["nested"].append(2)
    assert original["other"]["nested"] == [1]


@pytest.mark.parametrize("value", [1, "abc", {}])
def test_bad_data(value):
    with pytest.raises(TransformationError):
        build().transform({"value": value})


def test_missing_null_and_bad_record():
    assert build().transform({}) == {}
    assert build().transform({"value": None}) == {"value": None}
    with pytest.raises(TransformationError):
        build().transform([])


@pytest.mark.parametrize(
    "options",
    [
        {"fields": []},
        {"fields": ["x", "x"]},
        {"unknown_option": True},
        {"step": 0},
        {"start": True},
        {"stop": "1"},
        {"step": None},
    ],
)
def test_bad_configuration(options):
    with pytest.raises(ConfigurationError):
        build(**options)
