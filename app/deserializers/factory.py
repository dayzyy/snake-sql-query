import deserializers.deserializers as deserializers_module
from deserializers.deserializers import BaseDeserializer
from deserializers.utils.inspect_deserializers import extract_format_from_deserializer
from common.get_classes import get_classes

class DeserializerFactory:
    DESERIALIZERS: dict[str, type[BaseDeserializer]] = {
        extract_format_from_deserializer(cls): cls
        for cls in get_classes(BaseDeserializer, deserializers_module)
    }

    @classmethod
    def get_deserializer(cls, format: str) -> type[BaseDeserializer]:
        try:
            return cls.DESERIALIZERS[format.lower()]
        except KeyError:
            raise ValueError(
                "Unsupported format!\n"
                f"Deserialization supported formats: {list(cls.DESERIALIZERS.keys())}"
            )
