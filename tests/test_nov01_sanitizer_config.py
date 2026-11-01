import pytest

from etl_wore.transformers.sanitizer import DataSanitizer


@pytest.mark.parametrize(
    "options",
    [{"mask_fields": "secret"}, {"mask_fields": [1]}, {"strip_strings": "false"}],
)
def test_bad_sanitizer_settings_cannot_silently_disable_masking(options):
    with pytest.raises(ValueError):
        DataSanitizer(**options)


def test_masks_are_snapshotted():
    fields = ["secret"]
    sanitizer = DataSanitizer(mask_fields=fields)
    fields.clear()
    assert sanitizer.transform({"secret": "x"}) == {"secret": "***MASKED***"}
