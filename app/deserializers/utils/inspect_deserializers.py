import deserializers
from deserializers.base_deserializers import BaseDeserializer
import inspect
from typing import List, Type

def get_deserializer_classes():
    result: List[Type[BaseDeserializer]] = []

    for _, obj in inspect.getmembers(deserializers, inspect.isclass):
        if issubclass(obj, BaseDeserializer) and obj is not BaseDeserializer:
            result.append(obj)
