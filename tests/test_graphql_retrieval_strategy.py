import unittest
import vcr
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class TestGraphQLRetrievalStrategy(unittest.TestCase):
    @vcr.use_cassette('cassettes/test_retrieve_data_with_empty_filter.yaml')
    def test_retrieve_data_with_empty_filter(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://example.com/graphql")
        with self.assertRaises(Exception) as context:
            strategy.retrieve_data(filters={})
        self.assertEqual(str(context.exception), "Filters cannot be empty")

    @vcr.use_cassette('cassettes/test_retrieve_data_with_game_filter.yaml')
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
