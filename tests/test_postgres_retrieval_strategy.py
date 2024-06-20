import unittest
from telemetry.retrieval.postgres_retrieval_strategy import PostgresRetrievalStrategy

class TestPostgresRetrievalStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = PostgresRetrievalStrategy()

    def test_retrieve_data(self):
        query = "SELECT * FROM telemetry_game"  # Example query
        data = self.strategy.retrieve_data(query)
        self.assertIsNotNone(data)

    def test_games(self):
        result = self.strategy.games()
        self.assertIsInstance(result, list)
        game_names = [game[1] for game in result]  # Assuming the second column is the game name
        self.assertIn("iRacing", game_names)

    def test_sessions(self):
        result = self.strategy.sessions(limit=10)
        self.assertEqual(len(result), 10)

if __name__ == "__main__":
    unittest.main()
