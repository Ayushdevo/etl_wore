import json
import shutil
from pathlib import Path

from etl_wore.builder import build_pipeline
from etl_wore.spec_parser import SpecParser


def test_documented_customer_spec_runs_without_modification(tmp_path):
    root = Path(__file__).parents[1]
    for directory in ("examples", "fixtures"):
        shutil.copytree(root / directory, tmp_path / directory)
    path = tmp_path / "examples" / "customers.yaml"
    context = build_pipeline(SpecParser.parse_file(path), base_dir=path.parent).run()
    rows = [
        json.loads(line)
        for line in (tmp_path / "output" / "customers.jsonl").read_text().splitlines()
    ]
    assert len(rows) == 3
    assert all(row["email"] == "***MASKED***" for row in rows)
    assert all(isinstance(row["id"], int) for row in rows)
    assert rows[0]["signup_date"] == "2026-01-15T00:00:00Z"
    assert (context.records_extracted, context.records_loaded, context.records_dropped) == (4, 3, 1)
