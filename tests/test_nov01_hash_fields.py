import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="hash_fields", **options), _TRANSFORMERS, "transformer")


def test_hash_is_deterministic_and_unambiguous():
    import hashlib

    transform = build(fields=["id"], target="digest")
    result = transform.transform({"id": {"b": 2, "a": 1}})
    assert result["digest"] == hashlib.sha256(b'{"id":{"a":1,"b":2}}').hexdigest()
    assert transform.transform({"id": {"a": 1, "b": 2}})["digest"] == result["digest"]
    assert (
        transform.transform({"id": None})["digest"]
        != transform.transform({"id": "None"})["digest"]
    )
    for value in ({}, {"id": float("nan")}, {"id": {1: "bad"}}):
        with pytest.raises(TransformationError):
            transform.transform(value)


def test_unapproved_hash_fails_during_build():
    with pytest.raises(ConfigurationError):
        build(fields=["id"], target="digest", algorithm="md5")


def test_declarative_customer_cleanup_pipeline(tmp_path):
    import json

    from etl_wore.builder import build_pipeline

    source = tmp_path / "input.json"
    target = tmp_path / "output.jsonl"
    source.write_text(
        json.dumps(
            [
                {"Name": "  ADA  ", "status": "A", "score": 12.345},
                {"Name": "Bob", "status": "D", "score": -1},
            ]
        )
    )
    pipeline = build_pipeline(
        {
            "name": "cleanup",
            "batch_size": 1,
            "extractors": [{"type": "json", "filepath": str(source)}],
            "transformers": [
                {"type": "sanitize"},
                {"type": "rename_fields", "mapping": {"Name": "name"}},
                {"type": "string_case", "fields": ["name"]},
                {"type": "filter_value", "field": "status", "value": "A"},
                {
                    "type": "clamp_numbers",
                    "fields": ["score"],
                    "minimum": 0,
                    "maximum": 10,
                },
                {"type": "round_numbers", "fields": ["score"], "digits": 1},
                {"type": "constants", "values": {"source": "crm"}},
                {"type": "hash_fields", "fields": ["name"], "target": "key"},
                {"type": "drop_fields", "fields": ["status"]},
            ],
            "loaders": [{"type": "jsonl", "output_path": str(target)}],
        }
    )
    summary = pipeline.run().summary()
    rows = [json.loads(line) for line in target.read_text().splitlines()]
    assert summary["loaded"] == 1 and summary["dropped"] == 1
    assert (
        rows[0]["name"] == "ada"
        and rows[0]["score"] == 10
        and rows[0]["source"] == "crm"
    )
    assert len(rows[0]["key"]) == 64 and "status" not in rows[0]
