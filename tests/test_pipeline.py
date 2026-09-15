"""
End-to-end integration tests for ETL pipeline.
"""
import tempfile
import os
import json
from etl_wore.pipeline.engine import Pipeline
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.transformers.sanitizer import DataSanitizer
from etl_wore.loaders.csv_loader import CsvLoader

def test_full_pipeline_flow():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as src:
        src_data = [
            {"id": "1", "name": "  alpha  ", "secret": "abc"},
            {"id": "2", "name": "beta", "secret": "xyz"}
        ]
        json.dump(src_data, src)
        src_path = src.name

    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as dst:
        dst_path = dst.name

    try:
        pipeline = Pipeline("test_flow", batch_size=2)
        pipeline.add_extractor(JsonExtractor(src_path))
        pipeline.add_transformer(DataSanitizer(strip_strings=True, mask_fields=["secret"]))
        pipeline.add_loader(CsvLoader(dst_path))

        ctx = pipeline.run()
        assert ctx.records_extracted == 2
        assert ctx.records_loaded == 2

        with open(dst_path, "r") as f:
            content = f.read()
        assert "***MASKED***" in content
        assert "alpha" in content
    finally:
        os.remove(src_path)
        os.remove(dst_path)
