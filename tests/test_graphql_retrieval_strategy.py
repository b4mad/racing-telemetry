import unittest
from telemetry.retrieval.graphql_retrieval_strategy import GraphQLRetrievalStrategy

class TestGraphQLRetrievalStrategy(unittest.TestCase):
    def test_retrieve_data_with_empty_filter(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://example.com/graphql")
        with self.assertRaises(Exception) as context:
            strategy.retrieve_data(filters={})
        self.assertEqual(str(context.exception), "Filters cannot be empty")

    def test_retrieve_data_with_game_filter(self):
        strategy = GraphQLRetrievalStrategy(endpoint="http://telemetry.b4mad.racing:30050/graphql")
        filters = ['game']
        result = strategy.retrieve_data(filters=filters)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

if __name__ == '__main__':
    unittest.main()
