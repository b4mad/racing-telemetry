from telemetry.retrieval.retrieval_strategy import RetrievalStrategy
from telemetry.adapter.adapter import Adapter
from telemetry.adapter.transparent_adapter import TransparentAdapter

from typing import Optional

class Telemetry:
    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy
        self.filter = {}

    def set_filter(self, filter):
        self.filter = filter

    def get_data(self, adapter: Adapter = TransparentAdapter()):
        raw_data = self.strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)
