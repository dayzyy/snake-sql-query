from abc import ABC, abstractmethod

class BaseFileReader(ABC):
    @classmethod
    @abstractmethod
    def read(cls, file_path: str) -> str:
        raise NotImplementedError

# Supports reading from any text formatted file (JSON, XML, CSV etc.)
class TextFileReader(BaseFileReader):
    @classmethod
    def read(cls, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
