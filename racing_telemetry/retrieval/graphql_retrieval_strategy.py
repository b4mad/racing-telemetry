import os
from typing import Optional, Any, List, Dict
from gql import Client, gql
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from .retrieval_strategy import RetrievalStrategy

class GraphQLRetrievalStrategy(RetrievalStrategy):
    def __init__(self, endpoint: str = "") -> None:
        if not endpoint:
            endpoint = "http://telemetry.b4mad.racing:30050/graphql"
        self.endpoint: str = endpoint
        path_to_this_file: str = os.path.dirname(os.path.abspath(__file__))
        path_to_schema: str = os.path.join(path_to_this_file, 'schema.graphql')
        with open(path_to_schema) as f:
            schema_str: str = f.read()
        transport: RequestsHTTPTransport = RequestsHTTPTransport(url=self.endpoint, verify=True, retries=3)
        self.client: Client = Client(transport=transport, schema=schema_str)
        self.ds: DSLSchema = DSLSchema(self.client.schema)

    def retrieve_data(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not filters:
            raise Exception("Filters cannot be empty")

        result: List[Dict[str, Any]] = response.get("allTelemetryGames", {}).get("nodes", [])
        return result

    def _query(self, query: Any) -> Dict[str, Any]:
        # query.args(first=10)
        query = dsl_gql(DSLQuery(query))
        return self.client.execute(query)

    def games(self) -> List[Dict[str, Any]]:
        query = self.query_all_games()
        result = self._query(query)
        result = result.get("allTelemetryGames", {}).get("nodes", [])
        return result

    def query_all_games(self) -> Any:
        ds = self.ds
        query = ds.Query.allTelemetryGames
        # query.select(ds.TelemetryGamesConnection.totalCount)
        query.select(ds.TelemetryGamesConnection.nodes.select(ds.TelemetryGame.name))
        return query

    def sessions(self, group_by: Optional[str] = None) -> List[Dict[str, Any]]:
        ds = self.ds
        query = ds.Query.allTelemetrySessions
        if group_by:
            # query.select(ds.TelemetrySessionsConnection.nodes.select(
            #     ds.TelemetrySession.telemetryDriverByDriverId.select(
            #         ds.TelemetryDriver.name
            #     )
            # ))
            # also count the sessions
            query.select(ds.TelemetrySessionsConnection.nodes.select(
                ds.TelemetrySession.count
            ))
        else:
            query.select(ds.TelemetrySessionsConnection.nodes.select(
                ds.TelemetrySession.sessionId,
                ds.TelemetrySession.start,
                ds.TelemetrySession.end,
                # ds.TelemetrySession.telemetryDriverByDriverId.select(
                #     ds.TelemetryDriver.name
                # ),
            ))
        result = self._query(query)
        result = result.get("allTelemetrySessions", {}).get("nodes", [])
        return result
