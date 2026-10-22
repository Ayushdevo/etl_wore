from etl_wore.transformers.deduplicator import DeduplicationTransformer

def test_nested_json_keys_are_supported():
    dedup = DeduplicationTransformer(["key"])
    first = {"key": {"a": [1, 2], "b": "value"}}
    equivalent = {"key": {"b": "value", "a": [1, 2]}}
    different = {"key": {"a": [2, 1], "b": "value"}}
    assert dedup.transform(first) == first
    assert dedup.transform(equivalent) is None
    assert dedup.transform(different) == different
