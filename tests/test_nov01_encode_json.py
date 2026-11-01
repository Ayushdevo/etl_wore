import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="encode_json", **options), _TRANSFORMERS, "transformer")


def test_canonical_json_encoding_including_null():
    assert build(fields=["payload"]).transform({"payload": {"z": 2, "a": "é"}}) == {
        "payload": '{"a":"é","z":2}'
    }
    assert build(fields=["payload"]).transform({"payload": None}) == {"payload": "null"}
    for value in ({1: "x"}, {"n": float("nan")}, set([1])):
        with pytest.raises(TransformationError):
            build(fields=["payload"]).transform({"payload": value})


def test_bad_flag():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], sort_keys=1)
