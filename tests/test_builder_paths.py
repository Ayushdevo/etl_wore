from copy import deepcopy
import json
from pathlib import Path
import pytest
from etl_wore.builder import build_pipeline
from etl_wore.exceptions import ConfigurationError


def spec(source="in.json", target="out.jsonl"):
    return {"name": "relative", "extractors": [{"type": "json", "filepath": source}], "loaders": [{"type": "jsonl", "output_path": target}]}


def test_relative_paths_are_resolved_from_explicit_base(tmp_path, monkeypatch):
    root = tmp_path / "specs"
    root.mkdir()
    (root / "in.json").write_text('[{"id":1}]')
    monkeypatch.chdir(tmp_path)
    config = spec()
    before = deepcopy(config)
    build_pipeline(config, base_dir=root).run()
    assert json.loads((root / "out.jsonl").read_text()) == {"id": 1}
    assert config == before
    assert not (tmp_path / "out.jsonl").exists()


def test_build_does_not_open_sources_or_create_destinations(tmp_path):
    pipeline = build_pipeline(spec(), base_dir=tmp_path / "absent")
    assert pipeline.extractors[0].filepath == str(tmp_path / "absent" / "in.json")
    assert not (tmp_path / "absent").exists()


@pytest.mark.parametrize("target", ["in.json", "nested/../in.json"])
def test_input_output_collisions_are_rejected_before_io(tmp_path, target):
    with pytest.raises(ConfigurationError, match="input source"):
        build_pipeline(spec(target=target), base_dir=tmp_path)
    assert not any(tmp_path.iterdir())


def test_hard_link_alias_cannot_be_a_destination(tmp_path):
    source = tmp_path / "in.json"
    source.write_text('[{"id":1}]')
    alias = tmp_path / "out.jsonl"
    import os
    os.link(source, alias)
    with pytest.raises(ConfigurationError, match="input source"):
        build_pipeline(spec(), base_dir=tmp_path)
    assert source.read_text() == '[{"id":1}]'
