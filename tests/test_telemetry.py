import unittest
from telemetry import Telemetry
from telemetry.data_retrieval.data_retrieval_strategy import DataRetrievalStrategy
from telemetry.data_adapter.data_adapter import DataAdapter

class MockDataRetrievalStrategy(DataRetrievalStrategy):
    def retrieve_data(self, filters):
        return [{"key": "value"}]

class MockDataAdapter(DataAdapter):
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

if __name__ == '__main__':
    unittest.main()
