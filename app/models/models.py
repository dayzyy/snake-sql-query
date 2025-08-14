from fields.fields import Field

class Model:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        meta_data = {}

        meta_data['table_name'] = cls.__name__.lower() + 's'

        meta_data['fields'] = {
            name: value for name, value in cls.__dict__.items()
            if isinstance(value, Field)
        }

        cls._meta = meta_data
