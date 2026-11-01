import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="replace_text", **options), _TRANSFORMERS, "transformer"
    )


def test_literal_replacement_and_count():
    assert build(fields=["a"], old=".", new="-").transform({"a": "a.b.c"}) == {
        "a": "a-b-c"
    }
    assert build(fields=["a"], old=".", new="-", count=1).transform({"a": "a.b.c"}) == {
        "a": "a-b.c"
    }
    with pytest.raises(TransformationError):
        build(fields=["a"], old="x", new="y").transform({"a": 1})


@pytest.mark.parametrize("options", [{"old": ""}, {"count": True}, {"count": -1}])
def test_invalid_replace_config(options):
    kwargs = {"fields": ["a"], "old": "x", "new": "y"}
    kwargs.update(options)
    with pytest.raises(ConfigurationError):
        build(**kwargs)
