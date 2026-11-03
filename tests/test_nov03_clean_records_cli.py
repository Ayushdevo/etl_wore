"""Exercise the documented cleaning pipeline through real CLI processes and files."""

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("format", ["json", "yaml"])
def test_cleaning_example_from_another_directory(tmp_path, format):
    spec = json.loads((ROOT / "examples/clean_records.json").read_text())
    spec["extractors"][0]["filepath"] = str(ROOT / "fixtures/unclean_records.json")
    spec["loaders"][0]["output_path"] = "clean.jsonl"
    path = tmp_path / ("spec." + format)
    path.write_text(json.dumps(spec) if format == "json" else yaml.safe_dump(spec))
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    command = [sys.executable, "-m", "etl_wore", "--spec", str(path)]
    dry = subprocess.run(
        command + ["--dry-run"], cwd=elsewhere, capture_output=True, text=True
    )
    assert dry.returncode == 0, dry.stderr
    assert not (tmp_path / "clean.jsonl").exists()
    result = subprocess.run(
        command + ["--summary", "json"], cwd=elsewhere, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert (summary["extracted"], summary["loaded"], summary["dropped"]) == (1, 1, 0)
    assert json.loads((tmp_path / "clean.jsonl").read_text()) == {
        "name": "Café & Tea",
        "component": "a%2Fb%20c%2B",
        "message": "w6k=",
        "tags": ["a"],
        "length": 2,
        "id": "42",
        "active": False,
    }


def test_invalid_encoded_data_fails_without_output(tmp_path):
    data = tmp_path / "invalid.json"
    data.write_text('[{"component": "%FF"}]')
    spec = {
        "name": "invalid-encoding",
        "extractors": [{"type": "json", "filepath": "invalid.json"}],
        "transformers": [{"type": "url_decode", "fields": ["component"]}],
        "loaders": [{"type": "jsonl", "output_path": "out.jsonl"}],
    }
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    result = subprocess.run(
        [sys.executable, "-m", "etl_wore", "--spec", str(path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "component" in result.stderr
    assert not (tmp_path / "out.jsonl").exists()
