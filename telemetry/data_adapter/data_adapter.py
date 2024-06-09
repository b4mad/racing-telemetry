from abc import ABC, abstractmethod

class DataAdapter(ABC):
    @abstractmethod
    def convert(self, data):
        pass
