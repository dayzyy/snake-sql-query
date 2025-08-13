import deserializers
from deserializers.base_deserializers import BaseDeserializer
import inspect
from typing import List, Type

def get_deserializer_classes() -> List[Type[BaseDeserializer]]:
    result: List[Type[BaseDeserializer]] = []

    for _, obj in inspect.getmembers(deserializers, inspect.isclass):
        if issubclass(obj, BaseDeserializer) and obj is not BaseDeserializer:
            result.append(obj)

    return result

def extract_format_from_deserializer(cls: Type[BaseDeserializer]) -> str:
    name = cls.__name__
    if name.endswith("Deserializer"):
        return name[:-len("Deserializer")].lower()
    else:
        raise ValueError(
            "Deserializer class name must end with 'Deserializer'"
            "e.g: JSONDeserializer, XMLDeserializer, CSVDeserializer"
        )
