from abc import ABC, abstractmethod

class Adapter(ABC):
    @abstractmethod
    def convert(self, data):
        pass
