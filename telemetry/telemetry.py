from telemetry.retrieval import *
from telemetry.adapter.adapter import Adapter
from telemetry.adapter.transparent_adapter import TransparentAdapter

from typing import Optional

class Telemetry:
    def __init__(self):
        self.filter = {}

    def set_filter(self, filter):
        self.filter = filter

    def get_data(self, adapter: Adapter = TransparentAdapter()):
        raw_data = self.strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)

    def get_telemetry(self):
        self.strategy = InfluxRetrievalStrategy()
        return self.get_data()
