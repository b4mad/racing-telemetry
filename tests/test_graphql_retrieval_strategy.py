import unittest
import vcr
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class TestGraphQLRetrievalStrategy(unittest.TestCase):
    @vcr.use_cassette('tests/cassettes/test_retrieve_data_with_game_filter.yaml')
    def test_retrieve_data_with_game_filter(self):
        strategy = GraphQLRetrievalStrategy()
        filters = ['game']
        result = strategy.retrieve_data(filters=filters)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        game_names = [game['name'] for game in result]
        self.assertIn('iRacing', game_names)

if __name__ == '__main__':
    unittest.main()
