import sys
import pytest
from etl_wore.cli import main

@pytest.mark.parametrize("text", [None, "not json", "[]"])
def test_dry_run_rejects_invalid_spec(tmp_path, monkeypatch, text):
    path = tmp_path / "spec.json"
    if text is not None:
        path.write_text(text)
    monkeypatch.setattr(sys, "argv", ["etl-wore", "--spec", str(path), "--dry-run"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0

def test_dry_run_accepts_mapping(tmp_path, monkeypatch):
    path = tmp_path / "spec.json"
    path.write_text('{"name":"demo"}')
    monkeypatch.setattr(sys, "argv", ["etl-wore", "--spec", str(path), "--dry-run"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
