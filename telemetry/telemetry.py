from telemetry.retrieval import *
from telemetry.adapter import *

from typing import Optional

class Telemetry:
    def __init__(self):
        self.filter = {}
        self.graphql_strategy = GraphQLRetrievalStrategy()
        self.influx_strategy = InfluxRetrievalStrategy()
        self.adapter = TransparentAdapter()

    def set_pandas_adapter(self):
        self.adapter = PandasAdapter()

    def games(self):
        return self.adapter.convert(
            self.graphql_strategy.games()
        )

    def sessions(self):
        return self.adapter.convert(
            self.graphql_strategy.sessions()
        )

    def set_filter(self, filter):
        self.filter = filter

    def get_data(self, adapter: Adapter = TransparentAdapter()):
        self.strategy = GraphQLRetrievalStrategy()
        raw_data = self.strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)

    def get_data_df(self):
        return self.get_data(adapter=PandasAdapter())

    def get_telemetry(self, adapter: Adapter = TransparentAdapter()):
        self.strategy = InfluxRetrievalStrategy()
        raw_data = self.strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)

    def get_telemetry_df(self):
        return self.get_telemetry(adapter=PandasAdapter())
