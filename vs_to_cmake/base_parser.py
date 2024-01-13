from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, data: dict):
        self._data = data

    @abstractmethod
    def parse(self) -> str:
        pass
