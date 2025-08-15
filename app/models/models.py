from fields import fields
from common.get_classes import get_classes
from functools import partial
from dataclasses import dataclass
import sys
from db.db import Database

@dataclass
class Column:
    name: str
    field: fields.Field

class ModelMeta:
    def __init__(self, model: type["Model"]) -> None:
        self.model = model
        self.table_name = self._get_table_name()
        self.columns = self._get_table_columns()
        self.pk_column = self._get_table_pk_column()

    def _get_table_name(self):
        return self.model.__name__.lower() + 's'

    def _get_table_columns(self):
        return [
            Column(name, field) for name, field in self.model.__dict__.items()
            if isinstance(field, fields.Field)
        ]

    def _get_table_pk_column(self):
        pk_columns = [column for column in self.columns if column.field.pk]
        self._validate_columns_pk(pk_columns)

        return pk_columns[0]

    def _validate_columns_pk(self, columns: list[Column]):
        error = None
        if len(columns) < 1:
            error = (
                "Every model must have one primary key!\n"
                f"No primary key found in model {self.model.__name__!r}"
            )
        elif len(columns) > 1:
            error = (
                "Each model must have only one primary key!\n"
                f"Multiple primary keys found in model {self.model.__name__!r}:\n"
                f"{[column.name for column in columns]!r}"
            )
        if error:
            raise ValueError(error)

class Model:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls._meta = ModelMeta(cls)
        cls.manager = ModelManager(cls)
        cls.get_models = staticmethod(partial(get_classes, Model, sys.modules[cls.__module__]))

    def __init__(self, **kwargs) -> None:
        cls = self.__class__
        for column in cls._meta.columns:
            if column.name in kwargs:
                value = column.field._from_table_value(kwargs[column.name])
                setattr(self, column.name, value)
            elif column.field.default is not None:
                setattr(self, column.name, column.field.default)
            elif column.field.null:
                setattr(self, column.name, None)
            else:
                raise ValueError(f"Missing kwarg for {column.name!r} attribute in {cls.__name__}.__init__")

class ModelManager:
    def __init__(self, model: type[Model]) -> None:
        self.model = model
        
    def create(self):
        columns_sql = ', '.join(f"{col.name} {col.field.get_sql()}" for col in self.model._meta.columns)
        query = f"CREATE TABLE IF NOT EXISTS {self.model._meta.table_name} ({columns_sql})"

        Database.execute(query, commit=True)

    def add(self, row: Model):
        columns = [col.name for col in self.model._meta.columns]
        values = [getattr(row, col) for col in columns]

        placeholders = ', '.join(['%s'] * len(columns))
        columns_sql = ', '.join(columns)

        query = f"INSERT INTO {self.model._meta.table_name} ({columns_sql}) VALUES ({placeholders})"

        Database.execute(query, params=values, commit=True)
