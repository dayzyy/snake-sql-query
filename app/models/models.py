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

    def __init__(self, **kwargs) -> None:
        cls = self.__class__
        for name, field in cls._meta.fields.items():
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
