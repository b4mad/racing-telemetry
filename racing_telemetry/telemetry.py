from .retrieval import *
from .adapter import *

from typing import Optional, Any, Dict

class Telemetry:
    def __init__(self) -> None:
        self.filter: Dict[str, Any] = {}
        self.graphql_strategy: GraphQLRetrievalStrategy = GraphQLRetrievalStrategy()
        self.influx_strategy: InfluxRetrievalStrategy = InfluxRetrievalStrategy()
        self.postgres_strategy: PostgresRetrievalStrategy = PostgresRetrievalStrategy()
        self.adapter: Adapter = TransparentAdapter()

    def set_pandas_adapter(self) -> None:
        self.adapter = PandasAdapter()

    def games(self) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.games()
        )

    def sessions(self, group_by: Optional[str] = None, limit: Optional[int] = 10,
                 game: Optional[str] = None, track: Optional[str] = None, driver: Optional[str] = None) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.sessions(group_by=group_by, limit=limit, game_name=game, track_name=track, driver_name=driver)
        )

    def drivers(self) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.drivers()
        )

    def tracks(self, game: Optional[str] = None, track: Optional[str] = None) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.tracks(game_name=game, track_name=track)
        )

    def landmarks(self, game: Optional[str] = None, track: Optional[str] = None, kind: Optional[str] = None) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.landmarks(game_name=game, track_name=track, kind=kind)
        )

    def cars(self, game: Optional[str] = None) -> Any:
        return self.adapter.convert(
            self.postgres_strategy.cars(game=game)
        )

    def set_filter(self, filter: Dict[str, Any]) -> None:
        self.filter = filter

    def get_data(self, adapter: Adapter = TransparentAdapter()) -> Any:
        raw_data = self.graphql_strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)

    def get_data_df(self) -> Any:
        return self.get_data(adapter=PandasAdapter())

    def get_telemetry(self, adapter: Adapter = TransparentAdapter()) -> Any:
        self.strategy: InfluxRetrievalStrategy = InfluxRetrievalStrategy()
        raw_data = self.strategy.retrieve_data(self.filter)
        return adapter.convert(raw_data)

    def get_telemetry_df(self) -> Any:
        return self.get_telemetry(adapter=PandasAdapter())
