import os
from gql import Client, gql
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy

class GraphQLRetrievalStrategy(RetrievalStrategy):
    def __init__(self, endpoint = ""):
        if not endpoint:
            # endpoint = "http://telemetry.b4mad.racing:30050/graphql"
            endpoint = "https://rickandmortyapi.com/graphql"
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
        # query = self.ds.query.allTelemetryGames(
        #     self.ds.allTelemetryGames.totalCount(),
        #     self.ds.allTelemetryGames.nodes(
        #         self.ds.allTelemetryGames.nodes.name()
        #     )
        # )
        ds = self.ds
        # query = DSLQuery(
        #     ds.Query.characters.select(
        #         ds.Character.id
        #     )
        # )
        query = ds.Query.characters
        # query.select(ds.Character.id)
        # query.select(ds.Character.name)
        query = dsl_gql(DSLQuery(query))

        response = self.client.execute(query)
        result = response
        return result.get('allTelemetryGames', {}).get('nodes', [])
