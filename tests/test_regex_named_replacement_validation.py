import pytest
from etl_wore.transformers.regex_replace import RegexReplace
from etl_wore.builder import _component, _TRANSFORMERS
from etl_wore.exceptions import ConfigurationError
def test_unknown_named_backreference_has_configuration_error():
    with pytest.raises(ValueError):
        RegexReplace(['x'], '(a)', r'\g<missing>')
    with pytest.raises(ConfigurationError):
        _component({'type': 'regex_replace', 'fields': ['x'], 'pattern': '(a)', 'replacement': r'\g<missing>'}, _TRANSFORMERS, 'transformer')
