import re
import pytest
from fields import fields
from models.models import Model
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

@pytest.mark.parametrize(
    'ref_field',
    ['id', 'name']
)
def test_foreignkey_references_correct_field(ref_field: str):
    class Room(Model):
        id = fields.IntField(pk=True)
        name = fields.CharField()

    class Student(Model):
        id = fields.IntField(pk=True)
        room = fields.ForeignKey(Room, column_name=ref_field)

    assert Student.room.referenced_field == getattr(Room, ref_field)

def test_foreignkey_raises_if_referenced_field_not_found():
    class Room(Model):
        id = fields.IntField(pk=True)
        name = fields.CharField()

    with pytest.raises(ValueError, match=re.escape("Invalid reference: model 'Room' with column 'junk' does not exist or is not a Field!")):
        class Student(Model):
            id = fields.IntField(pk=True)
            room = fields.ForeignKey(Room, column_name='junk')
