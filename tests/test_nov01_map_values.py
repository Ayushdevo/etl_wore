import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="map_values", **options), _TRANSFORMERS, "transformer")


def test_category_mapping_and_unknown_policy():
    transform = build(field="status", mapping={"A": {"code": 1}})
    result = transform.transform({"status": "A"})
    assert result == {"status": {"code": 1}}
    result["status"]["code"] = 9
    assert transform.transform({"status": "A"})["status"]["code"] == 1
    assert transform.transform({"status": ["unknown"]}) == {"status": ["unknown"]}
    with pytest.raises(TransformationError):
        build(field="status", mapping={"A": 1}, strict=True).transform({"status": "B"})


def test_invalid_mapping():
    with pytest.raises(ConfigurationError):
        build(field="status", mapping=[])
