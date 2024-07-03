import unittest
import vcr
import pandas as pd
import json
import os
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

        # Initialize the Streaming class with all features enabled
        cls.streaming = Streaming(average_speed=True, coasting_time=True, raceline_yaw=True, ground_speed=True)

        # Process each row of the session data and collect features
        cls.collected_features = []
        for _, telemetry in cls.session_data.iterrows():
            cls.streaming.notify(telemetry)
            features = cls.streaming.get_features().copy()
            features['CurrentLapTime'] = telemetry['CurrentLapTime']
            features['Yaw'] = telemetry['Yaw']
            features['SpeedMs'] = telemetry['SpeedMs']
            cls.collected_features.append(features)

        # Save or load the collected features
        cls.features_file = 'tests/data/test_streaming.json'
        if not os.path.exists(cls.features_file):
            with open(cls.features_file, 'w') as f:
                json.dump(cls.collected_features, f, indent=4)
        else:
            with open(cls.features_file, 'r') as f:
                cls.expected_features = json.load(f)

    def test_average_speed(self):
        # Compare collected average_speed with expected values
        for i, (collected, expected) in enumerate(zip(self.collected_features, self.expected_features)):
            self.assertIn('average_speed', collected)
            self.assertIsInstance(collected['average_speed'], float)
            self.assertAlmostEqual(collected['average_speed'], expected['average_speed'], places=2,
                                    msg=f"Mismatch at index {i}")

    def test_coasting_time(self):
        # Compare collected coasting_time with expected values
        for i, (collected, expected) in enumerate(zip(self.collected_features, self.expected_features)):
            self.assertIn('coasting_time', collected)
            self.assertAlmostEqual(collected['coasting_time'], expected['coasting_time'], places=2,
                                       msg=f"Mismatch at index {i}")

        # Calculate total session time
        total_session_time = self.session_data['CurrentLapTime'].max() - self.session_data['CurrentLapTime'].min()

        # Coasting time should be less than or equal to total session time
        self.assertLessEqual(self.collected_features[-1]['coasting_time'], total_session_time)

    def test_raceline_yaw(self):
        # Compare collected raceline_yaw with expected values
        for i, (collected, expected) in enumerate(zip(self.collected_features, self.expected_features)):
            self.assertIn('raceline_yaw', collected)
            self.assertIsInstance(collected['raceline_yaw'], float)
            self.assertAlmostEqual(collected['raceline_yaw'], expected['raceline_yaw'], places=2,
                                   msg=f"Mismatch at index {i}")
            # Check if the yaw is within the expected range (-180 to 180 degrees)
            self.assertGreaterEqual(collected['raceline_yaw'], -180)
            self.assertLessEqual(collected['raceline_yaw'], 180)

    def test_ground_speed(self):
        # Compare collected ground_speed with expected values
        for i, (collected, expected) in enumerate(zip(self.collected_features, self.expected_features)):
            self.assertIn('ground_speed', collected)
            self.assertIsInstance(collected['ground_speed'], float)
            self.assertAlmostEqual(collected['ground_speed'], expected['ground_speed'], places=2,
                                   msg=f"Mismatch at index {i}")
            # Check if the ground speed is non-negative
            self.assertGreaterEqual(collected['ground_speed'], 0)

if __name__ == '__main__':
    unittest.main()
