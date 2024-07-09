import unittest
from racing_telemetry.retrieval.postgres_retrieval_strategy import PostgresRetrievalStrategy

class TestPostgresRetrievalStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = PostgresRetrievalStrategy()

    def test_retrieve_data(self):
        query = "SELECT * from telemetry_game"  # Example query
        data = self.strategy.retrieve_data(query)
        self.assertIsNotNone(data)

    def test_games(self):
        result = self.strategy.games()
        self.assertIsInstance(result, list)
        game_names = [game.name for game in result]  # Accessing the game name attribute directly
        self.assertIn("iRacing", game_names)

    def test_sessions(self):
        result = self.strategy.sessions(limit=10)
        self.assertEqual(len(result), 10)

    def test_sessions_group_by(self):
        result = self.strategy.sessions(limit=10, group_by="game_id")
        self.assertEqual(len(result), 10)

    def test_sessions_group_by_game(self):
        result = self.strategy.sessions(limit=10, group_by="game")
        self.assertEqual(len(result), 10)

if __name__ == "__main__":
    unittest.main()
