"""
Unit tests for transformers.
"""
from etl_wore.transformers.schema_validator import SchemaValidator
from etl_wore.transformers.sanitizer import DataSanitizer
from etl_wore.transformers.deduplicator import DeduplicationTransformer

def test_schema_validator():
    validator = SchemaValidator({"id": int, "score": float})
    res = validator.transform({"id": "42", "score": "98.5", "name": "Test"})
    assert res["id"] == 42
    assert res["score"] == 98.5

def test_sanitizer():
    sanitizer = DataSanitizer(strip_strings=True, mask_fields=["password"])
    res = sanitizer.transform({"username": "  alice  ", "password": "supersecret"})
    assert res["username"] == "alice"
    assert res["password"] == "***MASKED***"

def test_deduplicator():
    dedup = DeduplicationTransformer(key_fields=["email"])
    r1 = dedup.transform({"email": "test@example.com", "msg": "first"})
    r2 = dedup.transform({"email": "test@example.com", "msg": "second"})
    assert r1 is not None
    assert r2 is None
