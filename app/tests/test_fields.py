import pytest
from fields import fields
from typing import Any
from contextlib import nullcontext as does_not_raise
from datetime import datetime

@pytest.mark.parametrize(
    'field,value,expectation',
    [
        (fields.CharField(), 1, pytest.raises(ValueError)),
        (fields.IntField(), '1', pytest.raises(ValueError)),
        (fields.DateTimeField(), "2011-08-22T00:00:00.000000", does_not_raise()),
    ]
)
def test_fields_raise_on_invalid_value_type(field: fields.Field, value: Any, expectation):
    with expectation:
        field._validate(value)


@pytest.mark.parametrize(
    'field,value,expected_value',
    [
        (fields.CharField(), 'Luka', 'Luka'),
        (fields.IntField(), 1, 1),
        (fields.DateTimeField(), "2011-08-22T00:00:00.000000", datetime(year=2011, month=8, day=22, hour=0, minute=0, second=0, microsecond=0)),
    ]
)
def test_fields_handle_sql_table_values_correctly(field: fields.Field, value: Any, expected_value):
    assert field._from_table_value(value) == expected_value
