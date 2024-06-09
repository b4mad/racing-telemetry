import unittest
from telemetry import Telemetry

class TestTelemetry(unittest.TestCase):
    def test_initialization(self):
        telemetry = Telemetry()
        self.assertIsInstance(telemetry, Telemetry)

if __name__ == '__main__':
    unittest.main()
