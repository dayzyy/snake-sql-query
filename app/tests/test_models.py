import pytest
from models.models import Model
from models.models import Column
from fields import fields
import re

def test_model_raises_when_no_pk_field():
    with pytest.raises(
        ValueError,
        match=re.escape("Every model must have one primary key!\nNo primary key found in model 'Person'")
    ):
        class Person(Model):
            name = fields.CharField()
            age = fields.IntField()

def test_model_raises_when_multiple_pk_fields():
    with pytest.raises(
        ValueError,
        match=re.escape("Each model must have only one primary key!\nMultiple primary keys found in model 'Person':\n['name', 'age']")
    ):
        class Person(Model):
            name = fields.CharField(pk=True)
            age = fields.IntField(pk=True)

def test_model_raises_when_nonnull_field_not_provided_on_init():
    class Person(Model):
        name = fields.CharField(pk=True)
        age = fields.IntField(null=False)

    with pytest.raises(
        ValueError,
        match="Missing kwarg for 'age' attribute in Person.__init__"
    ):
        Person(name='Luka')

def test_model_meta_configs_correctly():
    name = fields.CharField(pk=True)
    age = fields.IntField(null=False)

    Person = type('Person', (Model,), {"name": name, "age": age, "junk": 1})

    assert Person._meta.model == Person
    assert Person._meta.columns == [Column("name", name), Column("age", age)]
    assert Person._meta.pk_column.name == 'name'
    assert Person._meta.pk_column.field == name
    assert Person._meta.table_name == 'persons'

    # The comparison:
    # Person._meta.columns == [Column("name", name), Column("age", age)]
    # Is valid, because Column uses the @dataclass decorator, which sets its __eq__ operator to compare by attribute values - not the object reference
