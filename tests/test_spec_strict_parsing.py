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
