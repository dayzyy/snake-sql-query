from typing import Type
from deserializers.deserializers import BaseDeserializer
from deserializers.utils.inspect_deserializers import get_deserializer_classes, extract_format_from_deserializer

class DeserializerFactory:
    DESERIALIZERS: dict[str, Type[BaseDeserializer]] = {
        extract_format_from_deserializer(cls): cls
        for cls in get_deserializer_classes()
    }

    @classmethod
    def get_deserializer(cls, format: str) -> Type[BaseDeserializer]:
        try:
            return cls.DESERIALIZERS[format.lower()]
        except KeyError:
            raise ValueError(
                "Unsupported format!\n"
                f"Deserialization supported formats: {list(cls.DESERIALIZERS.keys())}"
            )
