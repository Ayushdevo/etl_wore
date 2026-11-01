import json

import pytest

from etl_wore.cli import main


def test_output_cannot_overwrite_spec_even_in_dry_run(tmp_path):
    path = tmp_path / "pipeline.json"
    text = json.dumps(
        {
            "name": "safe",
            "extractors": [{"type": "json", "filepath": "input.json"}],
            "loaders": [{"type": "jsonl", "output_path": "pipeline.json"}],
        }
    )
    path.write_text(text)
    with pytest.raises(SystemExit) as error:
        main(["--spec", str(path), "--dry-run"])
    assert error.value.code == 2
    assert path.read_text() == text
