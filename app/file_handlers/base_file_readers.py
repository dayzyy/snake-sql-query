from abc import ABC, abstractmethod

class BaseFileReader(ABC):
    @classmethod
    @abstractmethod
    def read(cls, file_path: str):
        raise NotImplementedError
