from fields.fields import Field

class ModelMeta:
    def __init__(self, table_name: str, fields: dict[str, Field]) -> None:
        self.table_name = table_name
        self.fields = fields

class Model:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        table_name = cls.__name__.lower() + 's'

        fields = {
            name: value for name, value in cls.__dict__.items()
            if isinstance(value, Field)
        }

        cls._meta = ModelMeta(table_name, fields)
