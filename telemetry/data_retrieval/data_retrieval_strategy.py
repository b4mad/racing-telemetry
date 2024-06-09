from abc import ABC, abstractmethod

class DataRetrievalStrategy(ABC):
    @abstractmethod
    def retrieve_data(self, filters):
        pass
