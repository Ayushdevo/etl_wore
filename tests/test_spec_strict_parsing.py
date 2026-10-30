import pytest
from etl_wore.spec_parser import SpecParser
from etl_wore.exceptions import ConfigurationError


@pytest.mark.parametrize("text", ['{"name":"one","name":"two"}', '{"options":{"path":"a","path":"b"}}'])
def test_duplicate_json_keys_are_not_silently_overwritten(tmp_path, text):
    path = tmp_path / "pipeline.json"
    path.write_text(text)
    with pytest.raises(ConfigurationError, match="Duplicate specification key"):
        SpecParser.parse_file(path)
