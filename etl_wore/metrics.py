"""Write completed run metrics without leaving a partially written report."""
import json
import os
from pathlib import Path
import tempfile


def write_metrics(context, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=".etl-metrics-", delete=False) as file:
            temporary_path = file.name
            json.dump(context.summary(), file, ensure_ascii=False, allow_nan=False)
            file.write("\n")
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and os.path.exists(temporary_path):
            os.unlink(temporary_path)
