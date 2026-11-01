import pytest

from etl_wore.exceptions import ConfigurationError
from etl_wore.spec_parser import SpecParser


def test_recursive_sequence_alias_is_rejected(tmp_path):
    path = tmp_path / "pipeline.yaml"
    path.write_text("name: test\ncycle: &cycle [*cycle]\n")
    with pytest.raises(ConfigurationError, match="[Rr]ecursive"):
        SpecParser.parse_file(path)


def test_shared_nonrecursive_aliases_remain_valid(tmp_path):
    path = tmp_path / "pipeline.yaml"
    path.write_text("name: test\nfirst: &value [1, 2]\nsecond: *value\n")
    assert SpecParser.parse_file(path)["second"] == [1, 2]
