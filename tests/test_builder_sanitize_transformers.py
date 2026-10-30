from copy import deepcopy

import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def test_sanitizer_isolates_input_and_masks_selected_fields():
    stage = _component({"type": "sanitize", "mask_fields": ["ssn"]}, _TRANSFORMERS, "stage")
    record = {"name": " café ", "ssn": "secret"}
    before = deepcopy(record)
    assert stage.transform(record) == {"name": "café", "ssn": "***MASKED***"}
    assert record == before


@pytest.mark.parametrize(
    "options", [{"strip_strings": "false"}, {"mask_fields": "ssn"}, {"mask_fields": [None]}]
)
def test_sanitizer_configuration_is_typed(options):
    with pytest.raises(ConfigurationError):
        _component(dict(type="sanitize", **options), _TRANSFORMERS, "stage")
