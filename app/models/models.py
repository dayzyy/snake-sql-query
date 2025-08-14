from fields import fields
from common.get_classes import get_classes
from functools import partial
import sys

class ModelMeta:
    def __init__(self, table_name: str, columns: dict[str, fields.Field]) -> None:
        self.table_name = table_name
        self.columns = columns

class Model:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        table_name = cls.__name__.lower() + 's'

        columns = {
            name: value for name, value in cls.__dict__.items()
            if isinstance(value, fields.Field)
        }

        cls._meta = ModelMeta(table_name, columns)
        cls.get_models = staticmethod(partial(get_classes, Model, sys.modules[cls.__module__]))

    def __init__(self, **kwargs) -> None:
        cls = self.__class__
        for name, field in cls._meta.columns.items():
            if name in kwargs:
                value = kwargs[name]
                field.validate(value)
                setattr(self, name, value)
            elif field.default is not None:
                setattr(self, name, field.default)
            elif field.null:
                setattr(self, name, None)
            else:
                raise ValueError(f"Missing kwarg for {name!r} attribute in {cls.__name__}.__init__")
