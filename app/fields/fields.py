from abc import ABC

class Field(ABC):
    def __init__(self, pk: bool = False, fk: bool = False, unique: bool = False, null: bool = True, default=None) -> None:
        if pk and fk:
            raise ValueError("A field cannot be both primary key and foreign key.")

        self.pk = pk
        self.fk = fk

        if pk:
            self._set_primary_defaults()
        elif fk:
            self._set_foreign_defaults()
        else:
            self.unique = unique
            self.null = null
            self.default = default

    def _set_primary_defaults(self):
        # Defaults for a primary key column.
        self.unique = True
        self.null = False
        self.default = None

    def _set_foreign_defaults(self):
        # Defaults for a foreign key column.
        self.unique = False
        self.null = False
        self.default = None
