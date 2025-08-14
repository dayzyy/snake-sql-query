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

    @abstractmethod
    def get_python_type(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_sql_type(self) -> str:
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

    def validate(self, value) -> None:
        excepted_type = self.get_python_type()
        if not isinstance(value, excepted_type):
            raise ValueError(
                f"Invalid value type for {self.__class__.__name__!r} instance\n"
                f"Expected type: {excepted_type}\n"
                f"Provided type: {type(value)}"
            )

class IntField(Field):
    def get_python_type(self) -> type[int]:
        return int

    def get_sql_type(self) -> str:
        return "INTEGER"

class CharField(Field):
    def get_python_type(self) -> type[str]:
        return str

    def get_sql_type(self) -> str:
        return "VARCHAR"
