class Telemetry:
    def __init__(self):
        pass
from telemetry.data_retrieval.data_retrieval_strategy import DataRetrievalStrategy
from telemetry.data_adapter.data_adapter import DataAdapter

class Telemetry:
    def __init__(self, strategy: DataRetrievalStrategy):
        self.strategy = strategy
        self.filters = {}

    def set_filter(self, key, value):
        self.filters[key] = value

    def get_data(self, adapter: DataAdapter):
        raw_data = self.strategy.retrieve_data(self.filters)
        return adapter.convert(raw_data)
