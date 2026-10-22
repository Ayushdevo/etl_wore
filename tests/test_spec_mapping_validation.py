import pytest
from etl_wore.spec_parser import SpecParser
from etl_wore.exceptions import ConfigurationError

@pytest.mark.parametrize("suffix,text", [(".json","[]"), (".json","null"), (".json","{bad"), (".yaml",""), (".yaml","- item"), (".yaml","a: [")])
def test_bad_spec_raises_configuration_error(tmp_path, suffix, text):
    path = tmp_path / ("spec" + suffix)
    path.write_text(text)
    with pytest.raises(ConfigurationError):
        SpecParser.parse_file(str(path))

def test_mapping_is_returned(tmp_path):
    path = tmp_path / "spec.json"
    path.write_text('{"name": "demo"}')
    assert SpecParser.parse_file(str(path)) == {"name":"demo"}
