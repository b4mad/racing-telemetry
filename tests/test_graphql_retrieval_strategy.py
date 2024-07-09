import unittest
import vcr
from racing_telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class TestGraphQLRetrievalStrategy(unittest.TestCase):
    pass
    # @vcr.use_cassette('tests/cassettes/test_retrieve_data_with_game_filter.yaml')
    # def test_retrieve_data_with_game_filter(self):
    #     strategy = GraphQLRetrievalStrategy()
    #     filters = ['game']
    #     result = strategy.retrieve_data(filters=filters)
    #     self.assertIsInstance(result, list)
    #     self.assertIsInstance(result[0], dict)
    #     game_names = [game['name'] for game in result]
    #     self.assertIn('iRacing', game_names)
    #     # assert that we have 10 results
    #     self.assertEqual(len(result), 10)

    # @vcr.use_cassette('tests/cassettes/test_retrieve_data_with_session_filter.yaml')
    # def test_retrieve_data_with_session_filter(self):
    #     strategy = GraphQLRetrievalStrategy()
    #     filters = {'session': ['limit', 10]}
    #     result = strategy.retrieve_data(filters=filters)
    #     self.assertIsInstance(result, list)
    #     self.assertIsInstance(result[0], dict)
    #     game_names = [game['name'] for game in result]
    #     self.assertIn('iRacing', game_names)

    # # @vcr.use_cassette('tests/cassettes/test_sessions_group_by_game.yaml')
    # def test_sessions_group_by_game(self):
    #     strategy = GraphQLRetrievalStrategy()
    #     result = strategy.sessions(group_by='game')
    #     self.assertIsInstance(result, list)
    #     self.assertIsInstance(result[0], dict)
    #     game_sessions = {session['telemetryDriverByDriverId']['name']: session for session in result}
    #     self.assertIn('iRacing', game_sessions)
    #     # assert that we have sessions grouped by game
    #     self.assertGreaterEqual(len(game_sessions), 1)
