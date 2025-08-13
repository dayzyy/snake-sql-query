from abc import ABC, abstractmethod
from typing import Any

class BaseDeserializer(ABC):
    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> Any:
        # Convert raw string to standard python object list, dict etc.
        raise NotImplementedError
