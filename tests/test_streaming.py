import unittest
import vcr
import pandas as pd
from telemetry.analysis.streaming import Streaming
from telemetry.retrieval.influx_retrieval_strategy import InfluxRetrievalStrategy

class TestStreaming(unittest.TestCase):

    @classmethod
    @vcr.use_cassette('tests/cassettes/test_streaming_session_data.yaml')
    def setUpClass(cls):
        # Use InfluxRetrievalStrategy to get real data
        strategy = InfluxRetrievalStrategy()
        cls.session_data = strategy.retrieve_data(filters=1719855408)

        # Ensure we have data
        assert isinstance(cls.session_data, pd.DataFrame)
        assert len(cls.session_data) > 0

    def test_average_speed(self):
        # Initialize the Streaming class with average_speed enabled
        streaming = Streaming(average_speed=True)

        # Process each row of the session data
        for _, telemetry in self.session_data.iterrows():
            streaming.notify(telemetry)

        # Get the computed features
        features = streaming.get_features()

        # Check if average_speed is computed and is a reasonable value
        self.assertIn('average_speed', features)
        self.assertIsInstance(features['average_speed'], float)
        self.assertGreater(features['average_speed'], 0)
        self.assertLess(features['average_speed'], 500)  # Assuming speed is in m/s, 500 m/s is a reasonable upper limit

    def test_coasting_time(self):
        # Initialize the Streaming class with coasting_time enabled
        streaming = Streaming(coasting_time=True)

        # Process each row of the session data
        for _, telemetry in self.session_data.iterrows():
            streaming.notify(telemetry)

        # Get the computed features
        features = streaming.get_features()

        # Check if coasting_time is computed and is a reasonable value
        self.assertIn('coasting_time', features)
        self.assertIsInstance(features['coasting_time'], float)
        self.assertGreaterEqual(features['coasting_time'], 0)
        
        # Calculate total session time
        total_session_time = self.session_data['CurrentLapTime'].max() - self.session_data['CurrentLapTime'].min()
        
        # Coasting time should be less than or equal to total session time
        self.assertLessEqual(features['coasting_time'], total_session_time)

if __name__ == '__main__':
    unittest.main()
