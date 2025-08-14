from abc import ABC, abstractmethod
from typing import Any

class Field(ABC):
    def __init__(self, pk: bool = False, unique: bool = False, null: bool = True, default=None) -> None:
        if pk:
            unique = True
            null = False
            default = None

        self.pk = pk
        self.unique = unique
        self.null = null
        self.default = default

    @classmethod
    @abstractmethod
    def get_python_type(cls) -> Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_sql_type(cls) -> str:
        raise NotImplementedError

    def get_default_sql(self) -> str:
        parts = []

        if self.pk:
            parts.append('PRIMARY KEY')
        if self.unique:
            parts.append('UNIQUE')
        if not self.null:
            parts.append('NOT NULL')
        if self.default is not None:
            parts.append(f'DEFAULT "{self.default}"')

        sql = " ".join(parts)
        return sql

    def get_sql(self) -> str:
        return self.get_sql_type() + ' ' + self.get_default_sql()

class IntField(Field):
    @classmethod
    def get_python_type(cls):
        return int

    @classmethod
    def get_sql_type(cls) -> str:
        return "INTEGER"
