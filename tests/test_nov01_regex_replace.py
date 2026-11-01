import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="regex_replace", **options), _TRANSFORMERS, "transformer"
    )


def test_regex_groups_and_replacement_limits():
    assert build(
        fields=["a"], pattern=r"(\d+)", replacement=r"[\1]", count=1
    ).transform({"a": "x12 y34"}) == {"a": "x[12] y34"}
    with pytest.raises(TransformationError):
        build(fields=["a"], pattern="x", replacement="y").transform({"a": []})


@pytest.mark.parametrize("pattern,replacement", [("[", "x"), ("(a)", r"\2")])
def test_bad_patterns_or_groups_fail_during_build(pattern, replacement):
    with pytest.raises(ConfigurationError):
        build(fields=["a"], pattern=pattern, replacement=replacement)
