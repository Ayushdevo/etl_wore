import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="parse_json", **options), _TRANSFORMERS, "transformer")


def test_json_field_parsing_and_strict_numbers():
    assert build(fields=["payload"]).transform({"payload": '{"id":1}'}) == {
        "payload": {"id": 1}
    }
    for text in ('{"a":1,"a":2}', "NaN", "1e999", "{broken}"):
        with pytest.raises(TransformationError):
            build(fields=["payload"]).transform({"payload": text})
    assert build(fields=["payload"]).transform({"payload": "null"}) == {"payload": None}


def test_bad_fields():
    with pytest.raises(ConfigurationError):
        build(fields=[])
