import pytest
from etl_wore.transformers.deduplicator import DeduplicationTransformer
from etl_wore.exceptions import TransformationError
def test_cycle_reports_transformation_error_and_preserves_seen_state():
    cyclic = []; cyclic.append(cyclic)
    transformer = DeduplicationTransformer(['id'])
    with pytest.raises(TransformationError, match='key'):
        transformer.transform({'id': cyclic})
    assert transformer.transform({'id': [1]}) == {'id': [1]}
    assert transformer.transform({'id': [1]}) is None
def test_unhashable_key_is_a_transformation_error():
    with pytest.raises(TransformationError):
        DeduplicationTransformer(['id']).transform({'id': {1, 2}})
