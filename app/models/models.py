from fields import fields
from common.get_classes import get_classes
from functools import partial
from dataclasses import dataclass
import sys

@dataclass
class Column:
    name: str
    field: fields.Field

class ModelMeta:
    def __init__(self, table_name: str, columns: list[Column]) -> None:
        self.table_name = table_name
        self.columns = columns

class Model:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        table_name = cls.__name__.lower() + 's'
        columns = [Column(name, value) for name, value in cls.__dict__.items()]

        cls._meta = ModelMeta(table_name, columns)
        cls.get_models = staticmethod(partial(get_classes, Model, sys.modules[cls.__module__]))

    def __init__(self, **kwargs) -> None:
        cls = self.__class__
        for column in cls._meta.columns:
            if column.name in kwargs:
                value = kwargs[column.name]
                column.field.validate(value)
                setattr(self, column.name, value)
            elif column.field.default is not None:
                setattr(self, column.name, column.field.default)
            elif column.field.null:
                setattr(self, column.name, None)
            else:
                raise ValueError(f"Missing kwarg for {column.name!r} attribute in {cls.__name__}.__init__")
