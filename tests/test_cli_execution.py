import json
import subprocess
import sys

import pytest

from etl_wore.cli import main


def make_spec(tmp_path):
    (tmp_path / "input.csv").write_text("id,name\n1, Ada \n1, Duplicate \n2, Grace \n")
    spec = {
        "name": "customers",
        "batch_size": 1,
        "extractors": [{"type": "csv", "filepath": "input.csv"}],
        "transformers": [
            {"type": "sanitize"},
            {"type": "schema", "schema": {"id": "int"}},
            {"type": "deduplicate", "key_fields": ["id"]},
        ],
        "loaders": [{"type": "jsonl", "output_path": "out.jsonl"}],
    }
    path = tmp_path / "pipeline.json"
    path.write_text(json.dumps(spec))
    return path


def test_cli_executes_validated_pipeline_from_another_directory(tmp_path, monkeypatch):
    path = make_spec(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    assert main(["--spec", str(path)]) == 0
    assert [json.loads(line) for line in (tmp_path / "out.jsonl").read_text().splitlines()] == [
        {"id": 1, "name": "Ada"},
        {"id": 2, "name": "Grace"},
    ]


def test_dry_run_validates_components_without_writing(tmp_path):
    path = make_spec(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path), "--dry-run"])
    assert exc.value.code == 0
    assert not (tmp_path / "out.jsonl").exists()
    spec = json.loads(path.read_text())
    spec["loaders"][0]["typo"] = True
    path.write_text(json.dumps(spec))
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path), "--dry-run"])
    assert exc.value.code != 0


def test_failed_extraction_is_a_cli_error_without_output(tmp_path):
    path = make_spec(tmp_path)
    (tmp_path / "input.csv").unlink()
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path)])
    assert exc.value.code == 2
    assert not (tmp_path / "out.jsonl").exists()


def test_module_entry_point_runs_the_pipeline(tmp_path):
    path = make_spec(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "etl_wore", "--spec", str(path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert len((tmp_path / "out.jsonl").read_text().splitlines()) == 2


def test_json_summary_stdout_can_be_parsed_without_stripping_logs(tmp_path):
    path = make_spec(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "etl_wore", "--spec", str(path), "--summary", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["pipeline"] == "customers"
    assert (summary["extracted"], summary["loaded"], summary["dropped"]) == (3, 2, 1)
    assert "Starting pipeline" in result.stderr


@pytest.mark.parametrize("size", ["0", "-1"])
def test_invalid_batch_override_does_not_write(tmp_path, size):
    path = make_spec(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path), "--batch-size", size])
    assert exc.value.code == 2
    assert not (tmp_path / "out.jsonl").exists()


def test_batch_override_controls_flush_boundaries(tmp_path):
    from unittest.mock import patch

    from etl_wore.loaders.json_loader import JsonLinesLoader

    path = make_spec(tmp_path)
    batches = []
    real_load = JsonLinesLoader.load

    def observe(loader, records):
        batches.append(len(records))
        real_load(loader, records)

    with patch.object(JsonLinesLoader, "load", observe):
        main(["--spec", str(path), "--batch-size", "2"])
    assert batches == [2]


def test_metrics_report_matches_stdout(tmp_path):
    path = make_spec(tmp_path)
    metrics = tmp_path / "reports" / "run.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "etl_wore",
            "--spec",
            str(path),
            "--summary",
            "json",
            "--metrics-path",
            str(metrics),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(metrics.read_text()) == json.loads(result.stdout)


@pytest.mark.parametrize("target", ["pipeline.json", "input.csv", "out.jsonl"])
def test_metrics_cannot_overwrite_pipeline_files(tmp_path, target):
    path = make_spec(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path), "--metrics-path", str(tmp_path / target)])
    assert exc.value.code == 2
    assert not (tmp_path / "out.jsonl").exists()


def test_failed_metrics_replace_preserves_previous_report(tmp_path):
    from unittest.mock import patch

    from etl_wore.metrics import write_metrics
    from etl_wore.pipeline.context import PipelineContext

    path = tmp_path / "metrics.json"
    path.write_text("previous")
    with patch("etl_wore.metrics.os.replace", side_effect=OSError("full")):
        with pytest.raises(OSError):
            write_metrics(PipelineContext("test"), path)
    assert path.read_text() == "previous"
    assert list(tmp_path.iterdir()) == [path]


def test_invalid_metrics_path_is_a_cli_error_before_execution(tmp_path):
    path = make_spec(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main(["--spec", str(path), "--metrics-path", "bad\0path"])
    assert exc.value.code == 2
    assert not (tmp_path / "out.jsonl").exists()
