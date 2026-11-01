import pytest

from etl_wore.pipeline.engine import Pipeline


@pytest.mark.parametrize("method", ["add_extractor", "add_transformer", "add_loader"])
def test_registering_the_same_instance_twice_is_rejected(method):
    pipeline = Pipeline("duplicates")
    component = object()
    add = getattr(pipeline, method)
    assert add(component) is pipeline
    with pytest.raises(ValueError, match="already"):
        add(component)
