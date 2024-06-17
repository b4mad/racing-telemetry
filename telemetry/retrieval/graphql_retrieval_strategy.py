import os
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
#         query = gql("""
# query AllTelemetryGames {
#     allTelemetryGames {
#         totalCount
#         nodes {
#             name
#         }
#     }
# }
#         """)
        ds = self.ds
        # query = ds.Query.characters
        # query.select(ds.Characters.results.select(ds.Character.name))
        query = ds.Query.allTelemetryGames
        # query.select(ds.TelemetryGamesConnection.totalCount)
        query.select(ds.TelemetryGamesConnection.nodes.select(ds.TelemetryGame.name))
        query = dsl_gql(DSLQuery(query))

        response = self.client.execute(query)
        result = response
        print(result)
        return result
