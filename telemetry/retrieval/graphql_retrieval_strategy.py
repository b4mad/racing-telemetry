import os
from typing import Optional
from gql import Client, gql
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy

class GraphQLRetrievalStrategy(RetrievalStrategy):
    def __init__(self, endpoint = ""):
        if not endpoint:
            endpoint = "http://telemetry.b4mad.racing:30050/graphql"
        self.endpoint = endpoint
        path_to_this_file = os.path.dirname(os.path.abspath(__file__))
        path_to_schema = os.path.join(path_to_this_file, 'schema.graphql')
        with open(path_to_schema) as f:
            schema_str = f.read()
        transport = RequestsHTTPTransport(url=self.endpoint, verify=True, retries=3)
        self.client = Client(transport=transport, schema=schema_str)
        self.ds = DSLSchema(self.client.schema)

    def retrieve_data(self, filters):
        if not filters:
            raise Exception("Filters cannot be empty")

        result = response.get("allTelemetryGames", {}).get("nodes", [])
        return result

    def _query(self, query):
        # query.args(first=10)
        query = dsl_gql(DSLQuery(query))
        return self.client.execute(query)

    def games(self):
        query = self.query_all_games()
        result = self._query(query)
        result = result.get("allTelemetryGames", {}).get("nodes", [])
        return result

    def query_all_games(self):
        ds = self.ds
        query = ds.Query.allTelemetryGames
        # query.select(ds.TelemetryGamesConnection.totalCount)
        query.select(ds.TelemetryGamesConnection.nodes.select(ds.TelemetryGame.name))
        return query

    def sessions(self, group_by: Optional[str] = None):
        ds = self.ds
        query = ds.Query.allTelemetrySessions
        query.select(ds.TelemetrySessionsConnection.nodes.select(
            ds.TelemetrySession.sessionId,
            ds.TelemetrySession.start,
            ds.TelemetrySession.end,
            # ds.TelemetrySession.telemetryDriverByDriverId.select(
            #     ds.TelemetryDriver.name
            # ),
        ))
        if group_by:
            query.select(ds.TelemetrySessionsConnection.nodes.select(
                ds.TelemetrySession.telemetryDriverByDriverId.select(
                    ds.TelemetryDriver.name
                )
            ))
        result = self._query(query)
        result = result.get("allTelemetrySessions", {}).get("nodes", [])
        return result