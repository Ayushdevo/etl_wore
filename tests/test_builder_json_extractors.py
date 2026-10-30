import pytest
from etl_wore.builder import _component, _EXTRACTORS
from etl_wore.exceptions import ConfigurationError


@pytest.mark.parametrize("text,is_lines", [('[{"id":1},{"id":2}]', False), ('{"id":1}\n{"id":2}\n', True)])
def test_json_source_modes(tmp_path, text, is_lines):
    path = tmp_path / "records.json"
    path.write_text(text)
    source = _component({"type": "json", "filepath": str(path), "is_lines": is_lines}, _EXTRACTORS, "source")
    assert list(source.extract()) == [{"id": 1}, {"id": 2}]


def test_json_mode_requires_a_real_boolean():
    with pytest.raises(ConfigurationError, match="is_lines"):
        _component({"type": "json", "filepath": "records.json", "is_lines": "false"}, _EXTRACTORS, "source")
