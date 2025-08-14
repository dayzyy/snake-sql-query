import inspect
from typing import TypeVar

T = TypeVar('T')

def get_classes(cls: type[T], module):
    result: list[type[T]] = []

    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, cls) and obj is not cls:
            result.append(obj)

    return result
