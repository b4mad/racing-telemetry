from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy

class GraphQLRetrievalStrategy(RetrievalStrategy):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def retrieve_data(self, filters):
        # Implement GraphQL data retrieval logic here
        transport = RequestsHTTPTransport(url=self.endpoint, verify=True, retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
query AllTelemetryGames {
    allTelemetryGames {
        totalCount
        nodes {
            name
        }
    }
}
        """)
        # variables = {"filters": filters}
        response = client.execute(query)
        result = response
        return result.get('data', {}).get('data', [])
