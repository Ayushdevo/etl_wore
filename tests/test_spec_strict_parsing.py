import pytest
from etl_wore.spec_parser import SpecParser
from etl_wore.exceptions import ConfigurationError


@pytest.mark.parametrize("text", ['{"name":"one","name":"two"}', '{"options":{"path":"a","path":"b"}}'])
def test_duplicate_json_keys_are_not_silently_overwritten(tmp_path, text):
    path = tmp_path / "pipeline.json"
    path.write_text(text)
    with pytest.raises(ConfigurationError, match="Duplicate specification key"):
        SpecParser.parse_file(path)


@pytest.mark.parametrize("number", ["NaN", "Infinity", "-Infinity", "1e999"])
def test_nonfinite_json_options_are_rejected(tmp_path, number):
    path = tmp_path / "pipeline.json"
    path.write_text('{"option":' + number + '}')
    with pytest.raises(ConfigurationError):
        SpecParser.parse_file(path)


@pytest.mark.parametrize("suffix", ["json", "yaml"])
def test_utf8_bom_specifications(tmp_path, suffix):
    path = tmp_path / ("pipeline." + suffix)
    path.write_text('{"name":"café"}', encoding="utf-8-sig")
    assert SpecParser.parse_file(path) == {"name": "café"}


@pytest.mark.parametrize("text", ["name: one\nname: two\n", "options:\n  path: a\n  path: b\n"])
def test_duplicate_yaml_keys_are_rejected(tmp_path, text):
    path = tmp_path / "pipeline.yaml"
    path.write_text(text)
    with pytest.raises(ConfigurationError, match="Duplicate specification key"):
        SpecParser.parse_file(path)


def test_yaml_python_objects_are_not_constructed(tmp_path):
    path = tmp_path / "pipeline.yaml"
    path.write_text('!!python/object/apply:builtins.print ["unsafe"]')
    with pytest.raises(ConfigurationError):
        SpecParser.parse_file(path)


@pytest.mark.parametrize("text", ["1: value", "? [a, b]\n: value"])
def test_yaml_mapping_keys_must_be_strings(tmp_path, text):
    path = tmp_path / "pipeline.yaml"
    path.write_text(text)
    with pytest.raises(ConfigurationError, match="keys must be strings"):
        SpecParser.parse_file(path)
