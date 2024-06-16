import unittest
from telemetry import Telemetry
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class MockDataRetrievalStrategy(RetrievalStrategy):
    def retrieve_data(self, filters):
        return [{"key": "value"}]

class TestTelemetry(unittest.TestCase):

    def test_get_data(self):
        strategy = MockDataRetrievalStrategy()
        telemetry = Telemetry(strategy)
        data = telemetry.get_data()
        self.assertEqual(data, [{"key": "value"}])

    # def test_graphql_retrieval_strategy(self):
    #     strategy = GraphQLRetrievalStrategy(endpoint="http://telemetry.b4mad.racing:30050/graphql")
    #     telemetry = Telemetry(strategy)
    #     telemetry.set_filter("game")
    #     data = telemetry.get_data()
    #     self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
