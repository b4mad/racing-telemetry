import unittest
from telemetry import Telemetry
from telemetry.retrieval.retrieval_strategy import RetrievalStrategy
from telemetry.adapter.adapter import Adapter
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class MockDataRetrievalStrategy(RetrievalStrategy):
    def retrieve_data(self, filters):
        return [{"key": "value"}]

class MockDataAdapter(Adapter):
    def convert(self, data):
        return data

class TestTelemetry(unittest.TestCase):
    def test_initialization(self):
        strategy = MockDataRetrievalStrategy()
        telemetry = Telemetry(strategy)
        self.assertIsInstance(telemetry, Telemetry)

    def test_set_filter(self):
        strategy = MockDataRetrievalStrategy()
        telemetry = Telemetry(strategy)
        telemetry.set_filter("key", "value")
        self.assertEqual(telemetry.filters["key"], "value")

    def test_get_data(self):
        strategy = MockDataRetrievalStrategy()
        adapter = MockDataAdapter()
        telemetry = Telemetry(strategy)
        telemetry.set_filter("key", "value")
        data = telemetry.get_data(adapter)
        self.assertEqual(data, [{"key": "value"}])

    def test_graphql_retrieval_strategy(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://telemetry.b4mad.racing:30050/graphql")
        telemetry = Telemetry(strategy)
        telemetry.set_filter("game", "example_game")
        data = telemetry.get_data(MockDataAdapter())
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
