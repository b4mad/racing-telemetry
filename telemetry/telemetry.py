from telemetry.retrieval import *
from telemetry.adapter import *

from typing import Optional

class Telemetry:
    def __init__(self):
        self.filter = {}
        self.graphql_strategy = GraphQLRetrievalStrategy()
        self.influx_strategy = InfluxRetrievalStrategy()
        self.postgres_strategy = PostgresRetrievalStrategy(
            dbname="your_dbname",
            user="your_user",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        self.adapter = TransparentAdapter()

    def set_pandas_adapter(self):
        self.adapter = PandasAdapter()

    def games(self):
        return self.adapter.convert(
            self.graphql_strategy.games()
        )

    def sessions(self, group_by: Optional[str] = None):
        return self.adapter.convert(
            self.graphql_strategy.sessions(group_by=group_by)
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
