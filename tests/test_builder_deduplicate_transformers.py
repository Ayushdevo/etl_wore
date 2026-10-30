from etl_wore.builder import _component, _TRANSFORMERS


def test_deduplication_handles_nested_keys_and_fresh_runs():
    config = {"type": "deduplicate", "key_fields": ["key"]}
    first = _component(config, _TRANSFORMERS, "stage")
    record = {"key": {"a": [1, 2]}}
    assert first.transform(record) == record
    assert first.transform({"key": {"a": [1, 2]}, "extra": True}) is None
    second = _component(config, _TRANSFORMERS, "stage")
    assert second.transform(record) == record
