from etl_wore.transformers.deduplicator import DeduplicationTransformer


def test_missing_and_null_are_distinct_records():
    transform = DeduplicationTransformer(["id"])
    assert transform.transform({"name": "missing"}) == {"name": "missing"}
    assert transform.transform({"id": None}) == {"id": None}
    assert transform.transform({}) is None
    assert transform.transform({"id": None}) is None
