from abc import ABC, abstractmethod
from typing import Any, Optional

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

class ForeignKey(Field):
    from models.models import Model

    def __init__(
            self, model: Model, column_name: Optional[str] = None,
            pk: bool = False, unique: bool = False, null: bool = True, default=None
    ) -> None:

        super().__init__(pk=False, unique=False, null=False, default=None)

        self.model = model
        self.column_name = column_name
        self.referenced_field = self._get_referenced_field()


    def _get_referenced_field(self) -> Field:
        # Default the referenced column to the primary key column of the table
        ref_field = None
        if self.column_name is None:
            for name, field in self.model._meta.columns.items():
                if field.pk:
                    self.column_name = name
                    ref_field = field
        else:
            ref_field = getattr(self.model, self.column_name)

        if not ref_field:
            raise ValueError(f"Invalid reference: table {self.model._meta.table_name} with column {self.column_name!r} does not exist!")

        return ref_field

    def get_python_type(self) -> Any:
        return self.referenced_field.get_python_type()

    def get_sql_type(self) -> str:
        return self.referenced_field.get_sql_type()

    def get_sql(self) -> str:
        default = self.get_default_sql()
        fk_sql = f"REFERENCES {self.model._meta.table_name}({self.column_name})"

        return default + ' ' + fk_sql
