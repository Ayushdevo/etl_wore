import json

from etl_wore.builder import build_pipeline


def test_jsonl_sink_runs_a_complete_pipeline(tmp_path):
    source = tmp_path / "records.json"
    target = tmp_path / "out.jsonl"
    source.write_text('[{"id":1,"name":" café "},{"id":2,"name":" Jane "}]')
    spec = {
        "name": "clean",
        "batch_size": 1,
        "extractors": [{"type": "json", "filepath": str(source)}],
        "transformers": [{"type": "sanitize"}],
        "loaders": [{"type": "jsonl", "output_path": str(target)}],
    }
    ctx = build_pipeline(spec).run()
    assert [json.loads(line) for line in target.read_text().splitlines()] == [
        {"id": 1, "name": "café"},
        {"id": 2, "name": "Jane"},
    ]
    assert (ctx.records_extracted, ctx.records_loaded) == (2, 2)
