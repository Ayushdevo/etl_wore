import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="constants", **options), _TRANSFORMERS, "transformer")


def test_constants_attach_provenance_without_sharing_containers():
    transform = build(values={"source": ["crm"]})
    source = {"source": "old", "id": 1}
    result = transform.transform(source)
    assert result == {"source": ["crm"], "id": 1}
    result["source"].append("x")
    assert transform.transform({}) == {"source": ["crm"]}
    assert source["source"] == "old"
    with pytest.raises(TransformationError):
        build(values={"id": 2}, overwrite=False).transform(source)


def test_invalid_flag():
    with pytest.raises(ConfigurationError):
        build(values={"id": 1}, overwrite="false")
