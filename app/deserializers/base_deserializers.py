from abc import ABC, abstractmethod
from typing import Any
import json

class BaseDeserializer(ABC):
    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> Any:
        # Convert raw string to standard python object list, dict etc.
        raise NotImplementedError

class JSONDeserializer(BaseDeserializer):
    @classmethod
    def deserialize(cls, data: str) -> Any:
        return json.loads(data)
