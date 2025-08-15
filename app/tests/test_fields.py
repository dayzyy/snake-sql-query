import pytest
from fields import fields
from typing import Any
from contextlib import nullcontext as does_not_raise

@pytest.mark.parametrize(
    'field,value,expectation',
    [
        (fields.CharField(), 1, pytest.raises(ValueError)),
        (fields.IntField(), '1', pytest.raises(ValueError)),
        # (fields.DateTimeField(), "2011-08-22T00:00:00.000000", does_not_raise()),
    ]
)
def test_fields_raise_on_invalid_value_type(field: fields.Field, value: Any, expectation):
    with expectation:
        field.validate(value)
