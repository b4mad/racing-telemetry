from telemetry.retrieval.retrieval_strategy import RetrievalStrategy
from telemetry.adapter.adapter import Adapter

class Telemetry:
    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy
        self.filters = {}

    def set_filter(self, key, value):
        self.filters[key] = value

    def get_data(self, adapter: Adapter):
        raw_data = self.strategy.retrieve_data(self.filters)
        return adapter.convert(raw_data)
