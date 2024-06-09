from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy

class GraphQLRetrievalStrategy(RetrievalStrategy):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def retrieve_data(self, filters):
        if not filters:
            raise Exception("Filters cannot be empty")
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
        response = client.execute(query)
        result = response
        return result.get('allTelemetryGames', {}).get('nodes', [])
