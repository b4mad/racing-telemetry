import unittest
import vcr
import pandas as pd
from racing_telemetry.retrieval.influx_retrieval_strategy import InfluxRetrievalStrategy

class TestInfluxdbRetrievalStrategy(unittest.TestCase):

    @vcr.use_cassette('tests/cassettes/test_influx_retrieve_session.yaml')
    def test_retrieve_session(self):
        strategy = InfluxRetrievalStrategy()
        filters = 1718114100
        result = strategy.retrieve_data(filters=filters)
        self.assertIsInstance(result, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
