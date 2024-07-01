from telemetry.retrieval import *
from telemetry.adapter import *

from typing import Optional

class Telemetry:
    def __init__(self):
        self.filter = {}
        self.graphql_strategy = GraphQLRetrievalStrategy()
        self.influx_strategy = InfluxRetrievalStrategy()
        self.postgres_strategy = PostgresRetrievalStrategy()
        self.adapter = TransparentAdapter()

    def set_pandas_adapter(self):
        self.adapter = PandasAdapter()

    def games(self):
        return self.adapter.convert(
            self.postgres_strategy.games()
        )

    def sessions(self, group_by: Optional[str] = None, limit: Optional[int] = 10,
                 game: Optional[str] = None, track: Optional[str] = None, driver: Optional[str] = None):
        return self.adapter.convert(
            self.postgres_strategy.sessions(group_by=group_by, limit=limit, game_name=game, track_name=track, driver_name=driver)
        )

    def drivers(self):
        return self.adapter.convert(
            self.postgres_strategy.drivers()
        )

    def tracks(self, game: Optional[str] = None, track: Optional[str] = None):
        return self.adapter.convert(
            self.postgres_strategy.tracks(game_name=game, track_name=track)
        )

    def landmarks(self, game: Optional[str] = None, track: Optional[str] = None, kind: Optional[str] = None):
        return self.adapter.convert(
            self.postgres_strategy.landmarks(game_name=game, track_name=track, kind=kind)
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
