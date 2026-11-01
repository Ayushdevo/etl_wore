import pytest

from etl_wore.exceptions import ConfigurationError
from etl_wore.spec_parser import SpecParser


@pytest.mark.parametrize(
    "value", [".nan", ".inf", "2026-01-01", "!!set {a: null}", "!!binary aGVsbG8="]
)
def test_yaml_only_scalars_cannot_bypass_spec_contract(tmp_path, value):
    path = tmp_path / "pipeline.yaml"
    path.write_text("name: test\nvalue: " + value + "\n")
    with pytest.raises(ConfigurationError):
        SpecParser.parse_file(path)
