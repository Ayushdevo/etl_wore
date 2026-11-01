import json
import logging

import pytest

from etl_wore.cli import main


def test_verbose_reaches_pipeline_loggers_and_resets(tmp_path):
    path = tmp_path / "spec.json"
    path.write_text(
        json.dumps(
            {
                "name": "test",
                "extractors": [{"type": "json", "filepath": "input.json"}],
                "loaders": [{"type": "jsonl", "output_path": "output.jsonl"}],
            }
        )
    )
    for options, level in [(["--verbose"], logging.DEBUG), ([], logging.INFO)]:
        with pytest.raises(SystemExit):
            main(["--spec", str(path), "--dry-run"] + options)
        assert logging.getLogger("etl_wore.pipeline.engine").level == level
        assert logging.getLogger("etl_wore.utils.retry").level == level
